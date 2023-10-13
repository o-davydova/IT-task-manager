from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from task_hub.forms import TaskForm, TaskSearchForm
from task_hub.models import Task, TaskType


class IndexView(generic.View):
    def get(self, request):
        return HttpResponseRedirect(reverse_lazy("task-hub:task-list"))


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        form = TaskSearchForm(self.request.GET)
        queryset = Task.objects.all().select_related("task_type")

        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        num_assignee = self.object.assignees.count()
        context["num_assignee"] = num_assignee

        return context


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        return reverse("task-hub:task-detail", kwargs={'pk': self.object.pk})


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        return reverse_lazy("task-hub:task-detail", kwargs={'pk': self.object.pk})


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task-hub:task-list")


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType


class TaskTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = TaskType

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskTypeDetailView, self).get_context_data(**kwargs)
        num_tasks = self.object.tasks.count()
        context["num_tasks"] = num_tasks

        return context


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"

    def get_success_url(self):
        return reverse("task-hub:task-type-detail", kwargs={'pk': self.object.pk})


class CustomLogoutView(LogoutView):
    next_page = '/accounts/login'
