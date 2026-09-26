from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Task, SubTask


class TaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
    ordering = ["deadline"]

    def get_queryset(self):
        queryset = super().get_queryset()

        search_query = self.request.GET.get("search", "")

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        return queryset

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

class SubTaskCreateView(CreateView):
    model = SubTask
    template_name = "tasks/subtask_form.html"
    fields = ["title", "status"]

    def dispatch(self, request, *args, **kwargs):
        self.task = get_object_or_404(Task, pk=kwargs["task_pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.parent_task = self.task
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("task-detail", kwargs={"pk": self.task.pk})


class SubTaskUpdateView(UpdateView):
    model = SubTask
    template_name = "tasks/subtask_form.html"
    fields = ["title", "status"]

    def get_success_url(self):
        return reverse(
            "task-detail",
            kwargs={"pk": self.object.parent_task_id}
        )


class SubTaskDeleteView(DeleteView):
    model = SubTask
    template_name = "tasks/subtask_confirm_delete.html"

    def get_success_url(self):
        return reverse(
            "task-detail",
            kwargs={"pk": self.object.parent_task_id}
        )