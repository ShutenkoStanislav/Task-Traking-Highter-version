from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import uuid
from django.utils import timezone
from datetime import timedelta
import random
import string

def generate_invite_code():
    chars = string.ascii_letters + string.digits
    part1 = ''.join(random.choices(chars, k=4))
    part2 = ''.join(random.choices(chars, k=4))
    return f"{part1}-{part2}"



class Workspace(models.Model):
    INVITE_PERMISSION = [
        ("owner_only", "Only owner"),
        ("owner_admin", "Owner & Admin"),
                ]
    WORKSPACE_SPACE = [
        ("one", "Just me"),
        ("two_five", "Group (2-5)"),
        ("six_fifteen", "Team (6-15)"),
    ]

    SPACE_LIMITS = {
        "one": 1,
        "two_five": 5,
        "six_fifteen": 15,
    }

    name = models.CharField(max_length=64)
    invite_role = models.CharField(max_length=16,
                                choices=INVITE_PERMISSION,
                                default='owner_admin')
    workspace_space = models.CharField(max_length=16, choices=WORKSPACE_SPACE, default='one')
    icon = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User,
                            on_delete=models.CASCADE,
                            related_name='workspace_creator')
    

    def get_member_limit(self):
        return self.SPACE_LIMITS.get(self.workspace_space, 1)
    
    def get_active_member_count(self):
        return self.members.filter(is_active=True).count()

    def has_space(self):
        return self.get_active_member_count() < self.get_member_limit() 

    def get_admin_count(self):
        return self.members.filter(role='admin', is_active=True).count()

    def can_user_invite(self, user):
        try:
            membership = self.members.get(member=user, is_active=True)
        except WorkspaceMember.DoesNotExist:
            return False
        
        if membership.role == 'owner':
            return True
        if membership.role == 'admin' and self.invite_role == 'owner_admin':
            return True
        return False

    def __str__(self):
        return f"{self.name} - {self.owner}"
    
class WorkspaceMember(models.Model):
    MEMBER_PERMISSION = [
        ("owner", "Owner"),
        ("admin", "Admin"),
        ("member", "Member"),
                ]

    workspace = models.ForeignKey(Workspace,
                                on_delete=models.CASCADE, 
                                related_name="members")
    member = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='workspace_member')
    role = models.CharField(max_length=16, choices=MEMBER_PERMISSION, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        unique_together = ('workspace', 'member')

    def clean(self):
        if not self.pk and not self.workspace.has_space():
            raise ValidationError("You reach a workspace limite")
        
        if self.role == 'admin':
            admin_qs = WorkspaceMember.object.filter(
                workspace=self.workspace,
                role='admin',
                is_active = True
            ).exclude(pk=self.pk)

            if admin_qs.count() >= 4:
                raise ValidationError("Workspace limited to 4 admins maximum")
            

        if self.role == 'owner':
            owner_qs = WorkspaceMember.object.filter(
                workspace=self.workspace,
                role='owner',
                is_active = True
            ).exclude(pk=self.pk)
            if owner_qs.exists():
                raise ValidationError("Workspace limited to 1 owner maximum")
            
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.member} - {self.role}"
    
class WorkspaceInvite(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("declined", "Declined"),
        ("expired", "Expired"),
    ]

    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="invites"
    )
    invited_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_invites"
    )
    invited_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="received_invites"
    )
    code = models.CharField(
        max_length=9,
        unique=True,
        default=generate_invite_code
    )
    role = models.CharField(
        max_length=16,
        choices=WorkspaceMember.MEMBER_PERMISSION,
        default="member"
    )
    token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def is_valid(self):
        return self.status == "pending" and not self.is_expired()
    
    def mark_expired(self):
        self.status = "expired"
        self.save(update_fields=["status"])

    class Meta:
        ordering = ["-created_at"]
           
    

    def __str__(self):
        return f"Invite {self.code}-{self.workspace.name},  {self.status}"
        


class Box(models.Model):
    COLOR_VARIATION_BOX = [
        ("#123F73", "🔵Deep ocean"), 
        ("#D2A1FE", "🟣Violet"),
        ("#33DEB8", "🟢Aquamarine"),
        ("#6D020E", "🔴Red wine"),
        ("#FCF6A7", "🟡Sand"),
        ("#774C06", "🟤Terracotta"),
        ("#000000", "⚫Black"),
    ]

    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    name = models.CharField(max_length=24)
    color = models.CharField(max_length=32, choices=COLOR_VARIATION_BOX, default="#123F73")
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.workspace}"


class Folder(models.Model):

    COLOR_VARIATION = [
        ("#77acc7", "🔵Air blue"),
        ("#9966cc", "🟣Amethust"),
        ("#008000", "🟢Apple Green"),
        ("#ff033e", "🔴Red rose"),
        ("#ffe135", "🟡Banana yellow"),
        ("#ff6500", "🟠Sunset"),
        ("#000000", "⚫Black"),
    ]
    color = models.CharField(max_length=30, choices=COLOR_VARIATION, default="#77acc7")
    name = models.CharField(max_length=16)
    box = models.ForeignKey(Box, null=True, blank=True, on_delete=models.CASCADE, default=None, related_name='folders')
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, null=True, blank=True, default=None)
    
  

    def __str__(self):
        return self.name
    
class Task(models.Model):

    STATUS_CHOICES = [
        ("todo", "To Do"),
        ("in_progress", "In progress"),
        ("done", "Done"),
                ]
    
    PRIORITY_CHOICES = [
        ("low", "🟩Low"),
        ("medium", "🟨Medium"),
        ("high", "🟥High"),
                ]

    title = models.CharField(max_length=256)
    description = models.CharField(max_length=512)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="todo")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="low")
    due_date = models.DateField(null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trasks")
    created_at = models.DateTimeField(auto_now_add=True)
    folder = models.ForeignKey(
                Folder,
                on_delete=models.CASCADE,
                related_name="tasks",
                null=True,
                blank=True,
                default=None)
    
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return self.title
    

        
class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    media = models.FileField(upload_to="comments_media/", blank=True, null=True)

    def get_absolute_url(self):
        return self.task.get_absolute_url()