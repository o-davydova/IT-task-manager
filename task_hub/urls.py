from django.urls import path

from task_hub.views import TaskListView, IndexView, TaskDetailView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
]

app_name = "task-hub"
