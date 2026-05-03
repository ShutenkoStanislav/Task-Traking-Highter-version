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
            workspace=self.object,
            is_active=True
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
        name = request.POST.get("name")
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
def sended_invite(request, workspace_pk):
    if request.method != "POST":
        return JsonResponse({'error': "Method don't allowed"}, status=405)
    
    workspace = get_object_or_404(
        Workspace,
        pk=workspace_pk,
        members__member=request.user
    )

    if not workspace.can_user_invite(request.user):
        return JsonResponse({'error': "You don't have permission for invites"}, status=403)
    if not workspace.has_space():
        return JsonResponse({'error': f'Workspace reach the space limit ({workspace.get_member_limit()})'}, status=400)
    
    data = json.loads(request.body)
    role = data.get('role', 'member')
    
    if role not in ('member', 'admin'):
        return JsonResponse({'error':'Invalid role'}, status=400)
    
    user_role = workspace.members.get(member=request.user, is_active=True).role
    if role == 'admin' and user_role != 'owner':
        return JsonResponse({'error':'Only owner can promote member to Admin'}, status=403)
    
    if role == 'admin' and workspace.get_admin_count() >= 4:
        return JsonResponse({'error':'Workspace can only had 4 Admins'}, status=400)
    
    old_invite = WorkspaceInvite.objects.filter(
    workspace=workspace,
    invited_by=request.user,
    status='pending'
    ).first()
    if old_invite:
        old_invite.mark_expired()
    
    invite = WorkspaceInvite.objects.create(
        workspace=workspace,
        invited_by=request.user,
        role=role,
    )


    return JsonResponse({
        'success': True,
        'code': invite.code,
        'expires_in': '24 hours',     
    })

@login_required
def accept_invite(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    data = json.loads(request.body)
    code = data.get('code', '').strip().upper()

    invite = WorkspaceInvite.objects.filter(code=code).first()

    if not invite or not invite.is_valid():
       return JsonResponse({'error': 'Invalid or outdated code'}, status=400)
    
    workspace = invite.workspace

    if workspace.members.filter(member=request.user, is_active=True).exists():
        return JsonResponse({'error': 'You already part of this workspace'}, status=400)
    
    if not workspace.has_space():
        invite.mark_expired()
        return JsonResponse({'error': 'Workspace full'}, status=400)
       
    
    WorkspaceMember.objects.create(
        workspace=workspace,
        member=request.user,
        role=invite.role,
    )

    invite.invited_user = request.user
    invite.status = 'accepted'
    invite.save(update_fields=['invited_user', 'status'])

    return JsonResponse({
        'success': True,
        'workspace_id': workspace.pk,
        'workspace_name': workspace.name,
        'redirect_url': f'/workspace/{workspace.pk}/'
    })


@login_required
def decline_invite(request):
    data = json.loads(request.body)
    code = data.get('code', '').strip().upper()
    invite = get_object_or_404(WorkspaceInvite, code=code, status='pending')

    invite.status = 'declined'
    invite.save(update_fields=['status'])

    return JsonResponse({'success': True})

        
# Members

@login_required
def kick_member(request, workspace_pk, member_pk):
    if request.method != "POST":
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    workspace = get_object_or_404(Workspace, pk=workspace_pk)

    requester = get_object_or_404(
        WorkspaceMember,
        workspace=workspace,
        member=request.user,
        is_active=True
    )
    if requester.role != 'owner':
        return JsonResponse({'error': 'Only owner can kick members'}, status=403)
        
    if requester.pk == member_pk:
        return JsonResponse({'error': 'You connot kick yourself'}, status=400)

    target = get_object_or_404(
        WorkspaceMember,
        pk=member_pk,
        workspace=workspace,
        is_active=True   
    )

    if target.role == 'owner':
        return JsonResponse({'error': 'Cannot kick owner'}, status=400)
    
    target.is_active = False
    target.save(update_fields=['is_active'])

    return JsonResponse({'success': True})



@login_required
def promote_member(request, workspace_pk, member_pk):
    if request.method != "POST":
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    workspace = get_object_or_404(Workspace, pk=workspace_pk)

    requester = get_object_or_404(
        WorkspaceMember,
        workspace=workspace,
        member=request.user,
        is_active=True
    )

    if requester.role not in ('owner', 'admin'):
        return JsonResponse({'error': 'No permission'}, status=403)
    
    target = get_object_or_404(
        WorkspaceMember,
        pk=member_pk,
        workspace=workspace,
        is_active=True   
    )

    if target.role == 'owner':
        return JsonResponse({'error': 'Cannot change owner role'}, status=400)
    
    if requester.role == 'admin' and target.role == 'admin':
        return JsonResponse({'error': 'Admins cannot demote other admins'}, status=403)
    
    if target.role == 'member':
        if workspace.get_admin_count() >= 4:
            return JsonResponse({'error': 'Maximem 4 admins allowed'}, status=400)
        target.role = 'admin'
    else:
        target.role = 'member'

    target.save(update_fields=['role'])

    return JsonResponse({
        'success': True,
        'new_role': target.role
    })

        
