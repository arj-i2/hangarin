
from django.urls import path
from .views import (
    DashboardView,
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    SubTaskCreateView,
    SubTaskUpdateView,
    SubTaskDeleteView,
    NoteCreateView,
    NoteUpdateView,
    NoteDeleteView,
)

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),

    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("task/create/", TaskCreateView.as_view(), name="task-create"),
    path("task/<int:pk>/edit/", TaskUpdateView.as_view(), name="task-update"),
    path("task/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),

    path("task/<int:task_pk>/subtask/create/", SubTaskCreateView.as_view(), name="subtask-create"),
    path("subtask/<int:pk>/edit/", SubTaskUpdateView.as_view(), name="subtask-update"),
    path("subtask/<int:pk>/delete/", SubTaskDeleteView.as_view(), name="subtask-delete"),

    path("task/<int:task_pk>/note/create/", NoteCreateView.as_view(), name="note-create"),
    path("note/<int:pk>/edit/", NoteUpdateView.as_view(), name="note-update"),
    path("note/<int:pk>/delete/", NoteDeleteView.as_view(), name="note-delete"),
]