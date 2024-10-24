from django.test import TestCase
from .models import Activity, Dashboard
from datetime import timedelta


class BasicTestCase(TestCase):
    def setUp(self):
        Activity.objects.create(
            activity_name="test activity",
            expected_period=timedelta(days=3),
            dashboard=Dashboard.objects.create(name="Test", slug="test"),
        )

    def test_activity_without_last_entry(self):
        activity = Activity.objects.get(activity_name="test activity")
        self.assertEqual(activity.last_entry, None)
        self.assertNotEqual(activity.activity_name, "Blargh")
