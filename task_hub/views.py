from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.views import generic

from task_hub.forms import UserLoginForm
from task_hub.models import Worker, Task, TaskType, Position


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task

    def get_queryset(self):
        return Task.objects.filter(assignees=self.request.user).select_related("task_type")


class CustomLogoutView(LogoutView):
    next_page = '/accounts/login'
