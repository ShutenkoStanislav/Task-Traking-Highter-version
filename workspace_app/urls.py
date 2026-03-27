from django.urls import path
from workspace_app import views 
from task_app import views as task_view

app_name = "workspace"

urlpatterns = [
    path('workspace/<int:pk>/folder/<int:folder_id>/', task_view.TaskListView.as_view(), name='workspace-folder'),
    path('workspace/<int:pk>/', views.WorkspaceDetailView.as_view(), name="workspace_detail"),
    path('workspace/create/', views.WorkspaceCreateView.as_view(), name="workspace_create"),
    path('workspace/<int:pk>/delete/', views.WorkspaceDeleteView.as_view(), name="workspace_delete"),
    path('workspace/<int:pk>/update/', views.WorkspaceUpdateView.as_view(), name="workspace_update"),

    path('box/<int:pk>/', views.BoxDetailView.as_view(), name="box_detail"),
    path('workspace/<int:workspace_pk>/box/create/', views.BoxCreateView.as_view(), name="box_create"),
    path('box/<int:pk>/delete/', views.BoxDeleteView.as_view(), name="box_delete"),
    path('box/<int:pk>/update/', views.BoxUpdateView.as_view(), name="box_update"),
]