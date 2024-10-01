from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now
from dashboard.models import Activity, User
from datetime import timedelta


class TestIndexView(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="testuser", first_name="user", password="2137"
        )
        self.client.login(username="testuser", password="2137")

    def test_empty_dashboard(self):
        response = self.client.get(reverse("dashboard:index"))
        self.assertRegex(response.content, b"No activities defined.")


class TestTwoActivitiesIndexView(TestCase):
    def setUp(self):
        Activity.objects.create(
            activity_name="test activity",
            expected_period=timedelta(days=1),
            date_created=now() - timedelta(days=4),
        )
        Activity.objects.create(
            activity_name="test activity 2",
            expected_period=timedelta(days=1),
            date_created=now() - timedelta(days=8),
        )
        User.objects.create_user(
            username="testuser", first_name="user", password="2137"
        )
        self.client.login(username="testuser", password="2137")

    def test_get_with_parameter(self):
        response = self.client.get(reverse("dashboard:index") + "?priority=cupcakes")
        objects = {o: o.priority for o in response.context["object_list"]}
        self.assertEqual(len(objects), 2)
        response = self.client.get(
            reverse("dashboard:index") + "?priority=6"
        )  # TODO I bet there's a better way to do this
        objects = {o: o.priority for o in response.context["object_list"]}
        self.assertEqual(len(objects), 1)
        response = self.client.get(reverse("dashboard:index") + "?priority=9")
        objects = {o: o.priority for o in response.context["object_list"]}
        self.assertEqual(len(objects), 0)
