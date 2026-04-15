from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView
from task_app.models import Workspace, WorkspaceMember, Box, Folder
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from workspace_app.forms import BoxForm
from django.shortcuts import redirect ,get_object_or_404
from task_app.forms import TaskForm, FolderForm
import json



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

        context['task_form'] = TaskForm()
        context['folder_form'] = FolderForm()

        boxes_data = []
        for box in context['boxes']:
            boxes_data.append({
                'id': box.pk,
                'name': box.name,
                'folders': [
                    {'id': f.pk, 'name': f.name}
                    for f in box.folders.all()
                ]
            })
        context['boxes_json'] = json.dumps(boxes_data)

        return context


def workspace_create_view(request):
    if request.method == "POST":
        name = request.POST.get("workspace_name")
        workspace_space = request.POST.get("workspace_space")
        invite_role = request.POST.get("invite_role")

        if name:
            workspace = Workspace.objects.create(
                name=name,
                workspace_space=workspace_space,
                invite_role=invite_role,
                owner=request.user
            )
            WorkspaceMember.objects.create(
                workspace=workspace,
                member=request.user,
                role="owner"
            )
            return redirect('workspace:workspace_detail', pk=workspace.pk)
    return redirect('tasks:task_list')



    

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


def folder_create_view(request):
    if request.method == "POST":
        name=request.POST.get("name")
        color = request.POST.get("color", '#77acc7')
        box_id = request.POST.get("box_id")  
        
        if box_id:
            
            box = get_object_or_404(Box, pk=box_id)

            is_member = box.workspace.members.filter(member=request.user).exists()
            is_owner = box.workspace.owner == request.user

            if not is_member and not is_owner:
                return redirect('tasks:task_list')

            if name:
                Folder.objects.create(
                    name=name,
                    box=box,
                    workspace=box.workspace,
                    creator=request.user,
                    color=color
                )

            return redirect('workspace:workspace_detail', pk=box.workspace.pk)
        else:
          
            if name:   
                Folder.objects.create(
                    name=name,
                    creator=request.user,
                    color=color
                )       
            return redirect('tasks:task_list')
    
    return redirect('tasks:task_list')
