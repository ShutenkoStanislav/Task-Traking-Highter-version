from django.contrib import admin
from .models import Task, Folder, Workspace, Box

admin.site.register(Task)
admin.site.register(Folder)
admin.site.register(Workspace)
admin.site.register(Box)

# Register your models here.
