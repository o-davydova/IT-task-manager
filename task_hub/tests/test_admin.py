from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from task_hub.models import Position


class AdminSiteTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        position = Position.objects.create(name="position")

        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin",
            position=position
        )
        self.client.force_login(self.admin_user)

        self.worker = get_user_model().objects.create_user(
            username="worker",
            password="testworker",
            position=position
        )

    def test_worker_position_listed(self):
        url = reverse("admin:task_hub_worker_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.worker.position)

    def test_worker_detail_position_listed(self):
        url = reverse("admin:task_hub_worker_change", args=[self.worker.id])
        response = self.client.get(url)
        self.assertContains(response, self.worker.position)
