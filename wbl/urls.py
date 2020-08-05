from django.urls import path, re_path
from . import views

app_name = 'wbl'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('tasks/', views.tasks, name='tasks'),
    path('task-add/', views.task_add, name='task_add'),
    path('task-edit/', views.task_edit, name='task_edit'),
    path('task-detail/', views.task_detail, name='task_detail'),
    path('peer-review/', views.peer_review, name='peer_review'),
]