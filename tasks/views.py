from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Task


class TaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
    ordering = ["deadline"]


class TaskDetailView(DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"

class TaskCreateView(CreateView):
    model = Task
    template_name = "tasks/task_form.html"
    fields = "__all__"
    success_url = reverse_lazy("task-list")

class TaskUpdateView(UpdateView):
    model = Task
    template_name = "tasks/task_form.html"
    fields = "__all__"
    success_url = reverse_lazy("task-list")

class TaskDeleteView(DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("task-list")