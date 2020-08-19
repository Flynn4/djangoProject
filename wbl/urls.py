from django.urls import path, re_path
from . import views

app_name = 'wbl'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('tasks/', views.tasks, name='tasks'),
    path('task-add/', views.task_add, name='task_add'),
    path('add-task/', views.add_task, name='add_task'),
    re_path(r'^tasks/(\d+)/edit$', views.task_edit, name='task_edit'),
    re_path(r'^tasks/(\d+.)$', views.task_detail, name='task_detail'),
    re_path(r'^tasks/(\d+)/evaluations$', views.evaluations, name='evaluations'),
    re_path(r'^tasks/(\d+)/peer-review$', views.peer_review, name='peer_review'),
    path('evaluation-list/', views.evaluation_list, name='evaluation_list'),
    re_path(r'^tasks/(\d+)/peer-review-detail$', views.peer_review_detail, name='peer_review_detail'),
    re_path(r'^tasks/(\d+)/evaluation-mentor$', views.evaluation_mentor, name='evaluation_mentor'),
    re_path(r'^tasks/(\d+)/academic-evaluation$', views.academic_evaluation, name='academic_evaluation'),
    path('example-form/', views.example_form, name='example_form'),
    path('choose-role/', views.choose_role, name='choose_role'),
    path('get-choose-role/', views.get_choose_role, name='get_choose_role'),


]