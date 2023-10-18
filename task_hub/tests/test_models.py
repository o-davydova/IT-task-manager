from django.test import TestCase
from django.contrib.auth import get_user_model

from task_hub.models import Position, TaskType, Task


class PositionModelTest(TestCase):
    def test_position_str(self):
        position = Position.objects.create(
            name="TestPosition",
        )

        self.assertEqual(str(position), position.name)


class WorkerModelTest(TestCase):
    def setUp(self):
        position = Position.objects.create(
            name="TestPosition",
        )
        self.user_data = {
            "username": "TestUser",
            "password": "TestUserPass",
            "first_name": "Test",
            "last_name": "User",
            "position": position,
        }

        get_user_model().objects.create_user(**self.user_data)

    def test_worker_str(self):
        worker = get_user_model().objects.first()

        self.assertEqual(
            str(worker),
            f"{worker.position} ({worker.first_name} {worker.last_name})",
        )


class TaskTypeModelTest(TestCase):
    def test_task_type_str(self):
        task_type = TaskType.objects.create(
            name="TestTaskType"
        )

        self.assertEqual(str(task_type), task_type.name)


class TaskModelTest(TestCase):
    def setUp(self):
        task_type = TaskType.objects.create(
            name="TestTaskType"
        )

        Task.objects.create(
            name="TestTask",
            description="TestDescription",
            deadline="2023-12-12",
            task_type=task_type
        )

    def test_task_str(self):
        task = Task.objects.first()

        self.assertEqual(
            str(task),
            f"{task.name} - {task.get_priority_display()}"
        )
