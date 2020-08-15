from django.urls import path, re_path
from . import views

app_name = 'wbl'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('tasks/', views.tasks, name='tasks'),
    path('task-add/', views.task_add, name='task_add'),
    re_path(r'^tasks/(\d+)/edit$', views.task_edit, name='task_edit'),
    re_path(r'^tasks/(\d+.)$', views.task_detail, name='task_detail'),
    path('peer-review/', views.peer_review, name='peer_review'),
    path('add-task/', views.add_task, name='add_task'),
    path('evaluation-list/', views.evaluation_list, name='evaluation_list'),
    path('evaluations/', views.evaluations, name='evaluations'),
    path('detailed-evaluation/', views.detailed_evaluation, name='detailed_evaluation'),
]