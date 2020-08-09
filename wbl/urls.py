from django.urls import path, re_path
from . import views

app_name = 'wbl'

urlpatterns = [
    path('', views.index, name='index'),
    path('tasks/', views.tasks, name='tasks'),

]