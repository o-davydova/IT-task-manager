from django.urls import path

from task_hub.views import (
    TaskListView,
    IndexView,
    TaskDetailView,
    TaskUpdateView,
    TaskDeleteView,
    TaskCreateView,
    TaskTypeListView,
    TaskTypeDetailView,
    TaskTypeUpdateView,
    TaskTypeCreateView,
    TaskTypeDeleteView,
    WorkerListView,
    WorkerDetailView,
    WorkerDeleteView,
    WorkerUpdateView,
    PositionListView,
    PositionDetailView,
    PositionUpdateView,
    PositionCreateView,
    PositionDeleteView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),

    path("task-types/", TaskTypeListView.as_view(), name="task-type-list"),
    path("task-types/create/", TaskTypeCreateView.as_view(), name="task-type-create"),
    path("task-types/<int:pk>/", TaskTypeDetailView.as_view(), name="task-type-detail"),
    path("task-types/<int:pk>/update/", TaskTypeUpdateView.as_view(), name="task-type-update"),
    path("task-types/<int:pk>/delete/", TaskTypeDeleteView.as_view(), name="task-type-delete"),

    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/<int:pk>/delete/", WorkerDeleteView.as_view(), name="worker-delete"),
    path("workers/<int:pk>/update/", WorkerUpdateView.as_view(), name="worker-update"),

    path("positions/", PositionListView.as_view(), name="position-list"),
    path("positions/create", PositionCreateView.as_view(), name="position-create"),
    path("positions/<int:pk>/", PositionDetailView.as_view(), name="position-detail"),
    path("positions/<int:pk>/update/", PositionUpdateView.as_view(), name="position-update"),
    path("positions/<int:pk>/delete/", PositionDeleteView.as_view(), name="position-delete"),
]

app_name = "task-hub"
