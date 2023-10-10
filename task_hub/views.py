from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect, render
from django.views import generic

from task_hub.models import Task, Worker


class IndexView(generic.View):
    def get(self, request):
        return redirect('task-hub:task-list')


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


class CustomLogoutView(LogoutView):
    next_page = '/accounts/login'
