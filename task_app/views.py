from django.shortcuts import render, get_object_or_404, redirect
from task_app import models
from .models import Folder
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from task_app.forms import TaskForm, TaskFilterForm, FolderForm, SinginForm, CommentForm
from task_app.mixins import UserIsOwner
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required

from django.contrib.auth import login



class TaskListView(LoginRequiredMixin, ListView):
    model = models.Task
    context_object_name = "tasks"
    template_name = "tasks/task_list.html"

    def get_queryset(self):
        queryset = models.Task.objects.filter(creator=self.request.user).prefetch_related('comments')

        folder_id = self.kwargs.get('folder_id')

        if folder_id:
            queryset = queryset.filter(folder_id=folder_id)
        else:
            queryset = queryset.filter(folder__isnull=True)
        
        status = self.request.GET.get('status')

        if status:
            queryset = queryset.filter(status__iexact=status)
        else:
           queryset = queryset.exclude(status__iexact="done")

        
        return queryset.order_by("due_date")
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["folders"] = Folder.objects.filter(creator=self.request.user)

        folder_id = self.kwargs.get('folder_id')
        if folder_id:
            context['current_folder'] = get_object_or_404(Folder, id=folder_id, creator=self.request.user)
        else:
            context['current_folder'] = None

        context["form"] = TaskFilterForm(self.request.GET)
        context["task_form"] = TaskForm()
        context["folder_form"] = FolderForm()

        context["comment_form"] = CommentForm()
        
        return context

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = models.Task
    context_object_name = "task"
    template_name = "tasks/task_detail.html"

    def get_queryset(self):
        return models.Task.objects.filter(creator=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        comment_form = CommentForm(request.POST, request.FILES)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)

            comment.creator = request.user
            comment.task = self.get_object()
            comment.save()

            next_url = request.META.get('HTTP_REFERER')
            if next_url:
                return HttpResponseRedirect(next_url)
            else:
                return redirect("tasks:task_list")
        else:
            context = self.get_context_data(object=self.object)
            context['comment_form'] = comment_form
            return self.render_to_response(context)

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = models.Task
    success_url = reverse_lazy('tasks:task_list')
    template_name = "tasks/task_form.html"
    form_class = TaskForm

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        if self.object.folder:
            return reverse_lazy('tasks:folder-tasks', kwargs={'folder_id': self.object.folder.id})
        return reverse_lazy('tasks:task_list')

    
class FolderCreateView(LoginRequiredMixin, CreateView):
    model = models.Folder
    context_object_name = "folders"
    success_url = reverse_lazy('tasks:task_list')
    template_name = "tasks/folder_form.html"
    form_class = FolderForm

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

  
    
class TaskCompleteView(LoginRequiredMixin,  View):
    def post(self, request, *args, **kwargs):
        task = get_object_or_404(models.Task, pk=self.kwargs.get("pk"), creator=self.request.user)
        task.status = "done"
        task.save()
        return JsonResponse({'status': 'success'})
    
    def get_object(self):
        task_id = self.kwargs.get("pk")
        return get_object_or_404(models.Task, pk=task_id)

    
class TaskUpdateView(LoginRequiredMixin,  UpdateView):
    model = models.Task
    fields = ["title", "description", "priority"] 

    def get_queryset(self):
        return models.Task.objects.filter(creator=self.request.user)
        
    
    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER') or reverse_lazy('tasks:task_list')
        

class TaskDeleteView(LoginRequiredMixin ,DeleteView):
    model = models.Task
    
    def get_queryset(self):
        return models.Task.objects.filter(creator=self.request.user)
        
    
    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER') or reverse_lazy('tasks:task_list')
    

class FolderDeleteView(LoginRequiredMixin ,DeleteView):
    model = models.Folder
    
    def get_queryset(self):
        return models.Folder.objects.filter(creator=self.request.user)
        
    
    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER') or reverse_lazy('tasks:task_list')

class CustomLoginView(LoginView):
    template_name = "auth/login.html"
    redirect_authenticated_user = True
        

    
class CustomLogoutView(LogoutView):
    next_page = "tasks:login"

class RegisterViews(CreateView):
    template_name = "auth/singin.html"
    form_class = SinginForm
   

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("tasks:task_list")


@login_required   
def profile_details(request):
    user = request.user

    context = {
        'user' : user,
    }

    return render(
        request,
        template_name='tasks/profile.html',
        context=context,

    )


