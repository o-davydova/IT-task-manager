from django.urls import path

from task_hub.views import TaskListView

urlpatterns = [
    path("", TaskListView.as_view(), name="task-list"),
]

app_name = "task-hub"
