from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Task, SubTask, Note
from django.views.generic import TemplateView
from django.utils import timezone
from django import forms


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

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["deadline"].widget = forms.DateInput(
            attrs={"type": "date"}
        )
        return form

class TaskUpdateView(UpdateView):
    model = Task
    template_name = "tasks/task_form.html"
    fields = "__all__"
    success_url = reverse_lazy("task-list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["deadline"].widget = forms.DateInput(
            attrs={"type": "date"}
        )
        return form
    
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

class NoteCreateView(CreateView):
    model = Note
    template_name = "tasks/note_form.html"
    fields = ["content"]

    def dispatch(self, request, *args, **kwargs):
        self.task = get_object_or_404(
            Task,
            pk=kwargs["task_pk"]
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.task = self.task
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "task-detail",
            kwargs={"pk": self.task.pk}
        )


class NoteUpdateView(UpdateView):
    model = Note
    template_name = "tasks/note_form.html"
    fields = ["content"]

    def get_success_url(self):
        return reverse(
            "task-detail",
            kwargs={"pk": self.object.task_id}
        )


class NoteDeleteView(DeleteView):
    model = Note
    template_name = "tasks/note_confirm_delete.html"

    def get_success_url(self):
        return reverse(
            "task-detail",
            kwargs={"pk": self.object.task_id}
        )

class DashboardView(TemplateView):
    template_name = "tasks/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tasks = Task.objects.all()
        today = timezone.localdate()

        context["total_tasks"] = tasks.count()

        context["pending_tasks"] = tasks.filter(
            status="Pending"
        ).count()

        context["in_progress_tasks"] = tasks.filter(
            status="In Progress"
        ).count()

        context["completed_tasks"] = tasks.filter(
            status="Completed"
        ).count()

        context["recent_tasks"] = tasks.order_by(
            "-created_at"
        )[:5]

        context["upcoming_tasks"] = tasks.filter(
            deadline__gte=today
        ).exclude(
            status="Completed"
        ).order_by("deadline")[:5]

        return context