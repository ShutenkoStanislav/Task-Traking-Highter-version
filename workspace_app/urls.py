from django.urls import path
from workspace_app import views


app_name = "workspace"

urlpatterns = [
    path('workspace/<int:pk>/', views.WorkspaceDetailView.as_view(), name="workspace_detail"),
    path('workspace/create/', views.WorkspaceCreateView.as_view(), name="workspace_create"),
    path('workspace/<int:pk>/delete/', views.WorkspaceDeleteView.as_view(), name="workspace_delete"),
    path('workspace/<int:pk>/update/', views.WorkspaceUpdateView.as_view(), name="workspace_update"),
]