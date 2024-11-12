from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_calendar, name='task_calendar'),
    path('create/<str:date>/', views.create_task, name='create_task'),
    path('tasks/', views.task_list, name='task_list'),
    path('<int:task_id>/', views.task_detail, name='task_detail'),
]

