from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from task_hub.forms import TaskForm
from task_hub.models import Task


class IndexView(generic.View):
    def get(self, request):
        return HttpResponseRedirect(reverse_lazy("task-hub:task-list"))


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task

    def get_queryset(self):
        return Task.objects.filter(assignees=self.request.user).select_related("task_type")


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


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task-hub:task-list")


class CustomLogoutView(LogoutView):
    next_page = '/accounts/login'
