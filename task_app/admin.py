from django.contrib import admin
from .models import Task, Folder, Workspace, Box, WorkspaceLog

admin.site.register(Task)
admin.site.register(Folder)
admin.site.register(Workspace)
admin.site.register(Box)
admin.site.register(WorkspaceLog)


# Register your models here.
