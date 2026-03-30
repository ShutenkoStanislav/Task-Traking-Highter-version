from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView
from task_app.models import Workspace, WorkspaceMember, Box, Folder
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from workspace_app.forms import BoxForm
from django.shortcuts import get_object_or_404



class WorkspaceDetailView(LoginRequiredMixin, DetailView):
    model = Workspace
    context_object_name = "workspace"
    template_name = "workspace/workspace_detail.html"

    def get_queryset(self):
        return Workspace.objects.filter(
            members__member=self.request.user
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tab'] = self.request.GET.get('tab', 'main')
        context['boxes'] = Box.objects.filter(
            workspace=self.object
            ).prefetch_related('folders')
        context['members'] = WorkspaceMember.objects.filter(
            workspace=self.object
        ).select_related('member')

        context['folders'] = Folder.objects.filter(
            creator=self.request.user,
            box__isnull=True
        )
        context['workspaces'] = Workspace.objects.filter(
            members__member=self.request.user
        )
        context['user_role'] = WorkspaceMember.objects.get(
            workspace=self.object,
            member=self.request.user
        ).role

        context["box_form"] = BoxForm()
        context["folders_count"] = Folder.objects.filter(workspace=self.object).count()

        return context

class WorkspaceCreateView(LoginRequiredMixin, CreateView):
    model = Workspace
    fields = ['name', 'workspace_space', 'invite_role']
    template_name = "workspace/workspace_form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)

        WorkspaceMember.objects.create(
            workspace=self.object,
            member=self.request.user,
            role="owner"
        )
        return response
    
    def get_success_url(self):
        return reverse_lazy('workspace:workspace_detail', kwargs={'pk': self.object.pk})

    

class WorkspaceDeleteView(LoginRequiredMixin ,DeleteView):
    model = Workspace  

    def get_queryset(self):
        return Workspace.objects.filter(owner=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('workspace:workspace_detail')
    

class WorkspaceUpdateView(LoginRequiredMixin,  UpdateView):
    model = Workspace
    fields = ["icon", "name", "invite_permission"] 

    def get_queryset(self):
        return Workspace.objects.filter(
            members__member=self.request.user,
            members__role__in=['owner', 'admin']
        )
    
    def get_success_url(self):
        return reverse_lazy('workspace:workspace_detail', kwargs={'pk': self.object.pk})
       

class BoxDetailView(LoginRequiredMixin, DetailView):
    model = Box
    context_object_name = 'box'
    template_name = "workspace/main_tab.html"

    def get_queryset(self):
        return Box.objects.filter(
            workspace__members__member=self.request.user
        )
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['box_folders'] = Folder.objects.filter(box=self.object)
        context['folders'] = Folder.objects.filter(
            creator=self.request.user,
            box__isnull=True
        )
        context['workspaces'] = Workspace.objects.filter(
            members__member=self.request.user
        )



        return context
    

class BoxCreateView(LoginRequiredMixin, CreateView):
    model = Box
    fields = ['name','color']
    template_name = "workspace/modal_box_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workspace'] = get_object_or_404(
            Workspace,
            pk=self.kwargs['workspace_pk'],
        )
        return context
    
    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.workspace = get_object_or_404(
            Workspace,
            pk=self.kwargs['workspace_pk'],
            members__member=self.request.user
        )
        
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('workspace:workspace_detail', kwargs={'pk': self.object.workspace.pk})


class BoxDeleteView(LoginRequiredMixin, DeleteView):
    model = Box  

    def get_queryset(self):
        return Box.objects.filter(
            workspace__members__member=self.request.user,
            workspace__members__role__in=['owner', 'admin']
        )
    
    def get_success_url(self):
        return reverse_lazy('workspace:workspace_detail', kwargs={'pk': self.object.workspace.pk})

class BoxUpdateView(LoginRequiredMixin, UpdateView):
    model = Box
    fields = ['name','color']

    def get_queryset(self):
        return Box.objects.filter(
            workspace__members__member=self.request.user,
            workspace__members__role__in=['owner', 'admin']
        )
    
    def get_success_url(self):
        return reverse_lazy('workspace:workspace_detail', kwargs={'pk': self.object.workspace.pk})


# Create your views here.
