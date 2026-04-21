from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView
from task_app.models import Workspace, WorkspaceMember, Box, Folder, WorkspaceInvite
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from workspace_app.forms import BoxForm
from django.shortcuts import redirect ,get_object_or_404
from task_app.forms import TaskForm, FolderForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
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

#Invites

@login_required
def sended_invite(request, worksapce_pk):
    if request.method != "POST":
        return JsonResponse({'error': "Method don't allowed"}, status=405)
    
    workspace = get_object_or_404(
        Workspace,
        pk=worksapce_pk,
        members__member=request.user
    )

    if not workspace.can_user_invite(request.user):
        return JsonResponse({'error': "You don't have permission for invites"}, status=403)
    if not workspace.has_space():
        return JsonResponse({'error': f'Workspace reach the space limit ({workspace.get_member_limit()})'}, status=400)
    
    data = json.loads(request.body)
    email = data.get('email', '').strip()
    role = data.get('role', 'member')

    if not email:
        return JsonResponse({'error':'Email required'})
    
    if role not in ('member', 'admin'):
        return JsonResponse({'error':'Invalid role'}, status=400)
    
    user_role = workspace.members.get(member=request.user, is_active=True).role
    if role == 'admin' and user_role != 'owner':
        return JsonResponse({'error':'Only owner can promote member to Admin'}, status=403)
    
    if role == 'admin' and workspace.get_admin_count() >= 4:
        return JsonResponse({'error':'Workspace can only had 4 Admins'}, status=400)
    
    existing_invite = WorkspaceInvite.objects.filter(
        workspace=workspace,
        email=email,
        status='pending'
    ).first()

    if existing_invite:
        if existing_invite.is_valid():
            return JsonResponse({'error':'This email is already invited'}, status=400)
        else:
            existing_invite.mark_expired()

    already_member = workspace.members.filter(
        member__email=email,
        is_active=True
    ).exists()

    if already_member:
        return JsonResponse({'error':'This user is already part of workspace'}, status=400)
    
    invite = WorkspaceInvite.objects.create(
        workspace=workspace,
        invited_by=request.user,
        email=email,
        role=role,
    )

    invite_link = request.build_absolute_uri(f'/invite/{invite.token}/')

    return JsonResponse({
        'success': True,
        'invite_link': invite_link,
        'message': f'Invited sended to {email}'
    })

@login_required
def accept_invite(request, token):
    invite = get_object_or_404(WorkspaceInvite, token=token)

    if not invite.is_valid():
        messages.error(request, 'This invite sended or outdated')
        return redirect('task:task_list')
    
    if invite.email != request.user.email:
        messages.error(request, 'This invite for another email')
        return redirect('tasks:task_list')
    
    workspace = invite.workspace

    if workspace.members.filter(member=request.user, is_active=True).exists():
        messages.info(request, f'You already part of "{workspace.name}"')
        return redirect('workspace:workspace_detail', pk=workspace.pk)
    
    if not workspace.has_space():
        invite.mark_expired()
        messages.error(request, 'Workspace is full')
        return redirect('tasks:task_list')
    
    WorkspaceMember.objects.create(
        workspace=workspace,
        member=request.user,
        role=invite.role,
    )

    invite.invited_user = request.user
    invite.status = 'accepted'
    invite.save(update_fields=['invited_user', 'status'])

    messages.success(request, f'You join to "{workspace.name}"')
    return redirect('workspace:workspace_detail', pk=workspace.pk)

@login_required
def decline_invite(request, token):
    invite = get_object_or_404(
        WorkspaceInvite,
        token=token,
        status="pending",
    )

    if invite.email != request.user.email:
        messages.error(request, 'Its not for you')
        return redirect('tasks:task_list')
    
    invite.status = 'declined'
    invite.save(update_fields=['status'])

    messages.info(request, f'Invite to "{invite.worksapce.name}" declined')
    return redirect('tasks:task_list')

        
