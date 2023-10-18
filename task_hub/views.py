from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from task_hub.forms import TaskForm, TaskSearchForm, WorkerSearchForm, WorkerCreationForm, WorkerChangeForm
from task_hub.models import Task, TaskType, Position


class IndexView(generic.View):
    def get(self, request):
        return HttpResponseRedirect(reverse_lazy("task-hub:task-list"))


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("login")


class RegisterView(generic.CreateView):
    form_class = WorkerCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")


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


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position


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


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"

    def get_success_url(self):
        return reverse("task-hub:task-type-detail", kwargs={'pk': self.object.pk})


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("task-hub:task-type-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = WorkerSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        form = WorkerSearchForm(self.request.GET)
        queryset = get_user_model().objects.all().select_related("position")

        if form.is_valid():
            return queryset.filter(username__icontains=form.cleaned_data["username"])
        return queryset


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerDetailView, self).get_context_data(**kwargs)
        num_tasks = self.object.tasks.count()
        context["num_tasks"] = num_tasks

        return context


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = WorkerChangeForm

    def get_success_url(self):
        return reverse("logout")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("task-hub:worker-list")
