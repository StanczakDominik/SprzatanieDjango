from django.test import TestCase
from dashboard.models import Activity, Participant, Execution
from datetime import timedelta, datetime


class BasicTestCase(TestCase):
    def setUp(self):
        activity = Activity.objects.create(
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

class OneActionTestCase(TestCase):
    def setUp(self):
        activity = Activity.objects.create(
            activity_name="test activity", expected_period=timedelta(days=3)
        )
        participant = Participant.objects.create(participant_name="user")
        activity.execute(participant)

    def test_participant_name(self):
        participant = Participant.objects.get(participant_name="user")
        self.assertEqual(str(participant), "user")

    def test_priority(self):
        activity = Activity.objects.get(activity_name="test activity")
        self.assertLess(activity.priority, 1e-6)
        self.assertGreater(activity.priority, 0)

    def test_execution_str(self):
        execution = Execution.objects.get(id=1)
        self.assertRegex(str(execution), r"test activity done at .* by user")

