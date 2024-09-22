from django.test import TestCase
from django.urls import reverse
from dashboard.models import Activity, User, Execution
from datetime import timedelta


class BasicTestCase(TestCase):
    def setUp(self):
        Activity.objects.create(
            activity_name="test activity", expected_period=timedelta(days=3)
        )

    def test_activity_without_last_entry(self):
        activity = Activity.objects.get(activity_name="test activity")
        self.assertEqual(activity.last_entry, None)

    def test_activity_str_representation(self):
        activity = Activity.objects.get(activity_name="test activity")
        self.assertEqual(str(activity), "test activity")

    def test_activity_empty_priority(self):
        activity = Activity.objects.get(activity_name="test activity")
        self.assertEqual(activity.priority, 2137)

    def test_activity_appears_on_dashboard(self):
        response = self.client.get(reverse("dashboard:index"))
        self.assertEqual(len(response.context["activities"]), 1)

    def test_detail_view(self):
        response = self.client.get(reverse("dashboard:detail", args=[1]))
        self.assertEqual(response.context["activity"].activity_name, "test activity")


class OneActionTestCase(TestCase):
    def setUp(self):
        activity = Activity.objects.create(
            activity_name="test activity", expected_period=timedelta(days=3)
        )
        participant = User.objects.create(
            username="user", first_name="user", password="correcthorsebatterystaple"
        )
        activity.execute(participant)

    def test_priority(self):
        activity = Activity.objects.get(activity_name="test activity")
        self.assertLess(activity.priority, 1e-6)
        self.assertGreater(activity.priority, 0)

    def test_execution_str(self):
        execution = Execution.objects.get(id=1)
        self.assertRegex(str(execution), r"test activity done at .* by user")

    def test_detail_view(self):
        response = self.client.get(reverse("dashboard:detail", args=[1]))
        self.assertEqual(response.context["activity"].activity_name, "test activity")


class TestIndexView(TestCase):
    def test_empty_dashboard(self):
        response = self.client.get(reverse("dashboard:index"))
        self.assertRegex(response.content, b"No activities defined.")


class TestExecuteActivity(TestCase):
    def setUp(self):
        activity = Activity.objects.create(
            activity_name="test activity", expected_period=timedelta(days=3)
        )
        participant = User.objects.create(
            username="user", password="correcthorsebatterystaple"
        )
        activity.execute(participant)

    # # TODO test execute_activity... somehow
    # def test_execute_activity(self):
    #     fun = lambda: self.client.post("/dashboard/1/do", data={"participant": 1})
    #     fun()