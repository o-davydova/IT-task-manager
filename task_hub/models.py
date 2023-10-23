from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name="workers"
    )

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"
        ordering = ["position", ]

    def __str__(self):
        return f"{self.position} ({self.first_name} {self.last_name})"


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    class TaskPriority:
        low = "4"
        medium = "3"
        high = "2"
        urgent = "1"

    PRIORITY_CHOICES = (
        (TaskPriority.low, "Low"),
        (TaskPriority.medium, "Medium"),
        (TaskPriority.high, "High"),
        (TaskPriority.urgent, "Urgent"),
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=6,
        choices=PRIORITY_CHOICES,
        default=TaskPriority.medium,
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    assignees = models.ManyToManyField(Worker, related_name="tasks")

    class Meta:
        ordering = ["is_completed", "priority", "deadline"]

    def __str__(self):
        return f"{self.name} - {self.get_priority_display()}"
