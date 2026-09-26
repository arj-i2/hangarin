from django.urls import path
from .views import (
    TaskListView,
    TaskDetailView,
    TaskCreateView, 
    TaskUpdateView, 
    TaskDeleteView,
    SubTaskCreateView,
    SubTaskUpdateView,
    SubTaskDeleteView,
)
    

urlpatterns = [
    path("", TaskListView.as_view(), name="task-list"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("task/create/", TaskCreateView.as_view(), name="task-create"),
    path("task/<int:pk>/edit/", TaskUpdateView.as_view(), name="task-update"),
    path("task/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),

    path("task/<int:task_pk>/subtask/create/", SubTaskCreateView.as_view(), name="subtask-create"),
    path("subtask/<int:pk>/edit/", SubTaskUpdateView.as_view(), name="subtask-update"),
    path("subtask/<int:pk>/delete/", SubTaskDeleteView.as_view(), name="subtask-delete"),
]