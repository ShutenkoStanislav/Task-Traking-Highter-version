from django.db import models
from django.contrib.auth.models import User


class Workspace(models.Model):
    INVITE_PERMISSION = [
        ("admin", "Admin"),
        ("member", "Member"),
                ]
    WORKSPACE_SPACE = [
        ("one", "Just me"),
        ("two-five", "2-5"),
        ("six-fifteen", "6-15"),
    ]

    name = models.CharField(max_length=64)
    invite_role = models.CharField(max_length=16, choices=INVITE_PERMISSION, default='member')
    workspace_space = models.CharField(max_length=16, choices=WORKSPACE_SPACE, default='one')
    icon = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workspace_creator')

    def __str__(self):
        return f"{self.name} - {self.owner}"
    
class WorkspaceMember(models.Model):
    MEMBER_PERMISSION = [
        ("owner", "Owner"),
        ("admin", "Admin"),
        ("member", "Member"),
                ]

    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="members")
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workspace_member')
    role = models.CharField(max_length=16, choices=MEMBER_PERMISSION, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('workspace', 'member')

    def __str__(self):
        return f"{self.member} - {self.role}"
    
    


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
    color = models.CharField(max_length=32, choices=COLOR_VARIATION_BOX, default="Deep ocean")
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
    color = models.CharField(max_length=30, choices=COLOR_VARIATION, default="Black")
    name = models.CharField(max_length=16)
    box = models.ForeignKey(Box, null=True, blank=True, on_delete=models.CASCADE, default=None)
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