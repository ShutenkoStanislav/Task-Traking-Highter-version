from django.contrib import admin
from .models import Task, Folder, Workspace

admin.site.register(Task)
admin.site.register(Folder)
admin.site.register(Workspace)

# Register your models here.
