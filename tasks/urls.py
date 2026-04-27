from django.urls import path
from . import views 

app_name = "tasks"

urlpatterns = [
    path('', views.task_list, name="list"),
    path('<int:pk>/', views.task_detail, name="detail"),
    path('<int:pk>/delete/', views.task_delete, name="delete"),
    path('create/', views.task_create, name="create"),
    path('<int:pk>/status/', views.update_task, name="update_status"),
    path('<int:pk>/edit/', views.TaskUpdateView.as_view(), name='edit')
]