from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.views import generic

from task_hub.forms import UserLoginForm
from task_hub.models import Worker, Task, TaskType, Position


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = "task_hub/index.html"


class CustomLogoutView(LogoutView):
    next_page = '/accounts/login'
