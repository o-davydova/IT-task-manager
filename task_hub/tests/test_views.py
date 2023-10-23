from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_hub.models import Position, TaskType, Task

WORKER_URL = reverse("task-hub:worker-list")
TASK_TYPE_URL = reverse("task-hub:task-type-list")
TASK_URL = reverse("task-hub:task-list")
POSITION_URL = reverse("task-hub:position-list")


def create_test_user(
        username: str
) -> get_user_model():
    test_position = Position.objects.create(
        name=f"{username}TestPosition"
    )
    user = get_user_model().objects.create(
        username=username,
        password=f"{username}Pass",
        position=test_position
    )
    return user


def create_test_task(
        test_task_type: TaskType,
        name: str,
        assignees: list[get_user_model()]
) -> Task:
    test_task = Task.objects.create(
        name=name,
        description=f"{name}Description",
        deadline="2023-12-12",
        task_type=test_task_type,
    )
    for assignee in assignees:
        test_task.assignees.add(assignee)

    return test_task


class PublicAccessTest(TestCase):
    def test_worker_login_required(self):
        response = self.client.get(WORKER_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_task_type_login_required(self):
        response = self.client.get(TASK_TYPE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_task_login_required(self):
        response = self.client.get(TASK_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_position_login_required(self):
        response = self.client.get(POSITION_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateAccessTest(TestCase):
    def setUp(self):
        self.user = create_test_user("TestUser")
        self.client.force_login(self.user)

        worker1 = create_test_user("TestWorker1")
        worker2 = create_test_user("TestWorker2")

        test_task_type1 = TaskType.objects.create(name="TestTaskType1")
        test_task = create_test_task(test_task_type1, "TestTask", assignees=[worker1, worker2])

    def test_retrieve_task(self):
        response = self.client.get(TASK_URL)
        self.assertEqual(response.status_code, 200)

        tasks = Task.objects.all()
        self.assertEqual(
            list(response.context["task_list"]),
            list(tasks)
        )

        self.assertTemplateUsed(response, "task_hub/task_list.html")

    def test_retrieve_task_type(self):
        response = self.client.get(TASK_TYPE_URL)
        self.assertEqual(response.status_code, 200)

        task_types = TaskType.objects.all()
        self.assertEqual(
            list(response.context["tasktype_list"]),
            list(task_types)
        )

        self.assertTemplateUsed(response, "task_hub/tasktype_list.html")

    def test_retrieve_position(self):
        response = self.client.get(POSITION_URL)
        self.assertEqual(response.status_code, 200)

        positions = Position.objects.all()
        self.assertEqual(
            list(response.context["position_list"]),
            list(positions)
        )

        self.assertTemplateUsed(response, "task_hub/position_list.html")

    def test_retrieve_worker(self):
        response = self.client.get(WORKER_URL)
        self.assertEqual(response.status_code, 200)

        workers = get_user_model().objects.all()
        self.assertEqual(
            list(response.context["worker_list"]),
            list(workers)
        )

        self.assertTemplateUsed(response, "task_hub/worker_list.html")


class SearchingTest(TestCase):
    def setUp(self) -> None:
        self.user = create_test_user("TestUser")
        self.client.force_login(self.user)

        worker1 = create_test_user("TestWorker1")
        worker2 = create_test_user("TestWorker2")

        test_task_type1 = TaskType.objects.create(name="TestTaskType1")
        test_task_type2 = TaskType.objects.create(name="TestTaskType2")

        test_task1 = create_test_task(test_task_type1, "TestTask1", assignees=[worker1, worker2])
        test_task2 = create_test_task(test_task_type2, "TestTask2", assignees=[worker1])

    def test_task_name_search(self):
        search_parameter = {"name": "TestTask1"}
        response = self.client.get(TASK_URL, search_parameter)
        tasks = Task.objects.filter(
            name__icontains=search_parameter["name"]
        )

        self.assertEqual(list(tasks), list(response.context["task_list"]))

    def test_worker_username_search(self):
        search_parameter = {"username": "TestWorker1"}
        response = self.client.get(WORKER_URL, search_parameter)
        tasks = get_user_model().objects.filter(
            username__icontains=search_parameter["username"]
        )

        self.assertEqual(list(tasks), list(response.context["worker_list"]))
