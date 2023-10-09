from django.urls import path

from task_hub.views import TaskListView, IndexView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
]

app_name = "task-hub"
