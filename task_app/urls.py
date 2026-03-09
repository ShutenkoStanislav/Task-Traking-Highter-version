from django.urls import path
from task_app import views


app_name = "tasks"

urlpatterns = [
    path('', views.TaskListView.as_view(), name="task_list"),

    path('folder/<int:folder_id>/', views.TaskListView.as_view(), name='folder-tasks'),
    path('<int:pk>/', views.TaskDetailView.as_view(), name="task_detail"),

    path('<int:pk>/update/', views.TaskUpdateView.as_view(), name="task_update"),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name="task_delete"),

    path('folder/<int:pk>/delete/', views.FolderDeleteView.as_view(), name='folder_delete'),


    path('task-create/', views.TaskCreateView.as_view(), name="task-create"),
    path('folder-create/', views.FolderCreateView.as_view(), name="folder-create"),

    path('<int:pk>/complete/', views.TaskCompleteView.as_view(), name="task-complete"),

    path('login/', views.CustomLoginView.as_view(), name="login"),
    path('logout/', views.CustomLogoutView.as_view(), name="logout"),
    path('sing-in/', views.RegisterViews.as_view(), name="register"),
    
    path('profile/', views.profile_details, name="profile"),
    

]

