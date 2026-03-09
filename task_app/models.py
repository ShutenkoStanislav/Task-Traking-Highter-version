from django.db import models
from django.contrib.auth.models import User


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
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    
  

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

    


