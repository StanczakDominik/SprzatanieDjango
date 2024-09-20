from django.db import models
from datetime import datetime, timezone
from typing import Optional
from django.contrib.auth.models import User


class Activity(models.Model):
    activity_name = models.CharField(max_length=200)
    date_created = models.DateTimeField("date created", auto_now_add=True)
    expected_period = models.DurationField("expected period")

    @property
    def last_entry(self):
        try:
            return self.execution_set.order_by("-id")[0]
        except IndexError:
            return None

    def __str__(self, *args, **kwargs):
        return self.activity_name

    @property
    def priority(self):
        now = datetime.now(timezone.utc)

        last_entry = self.last_entry

        if last_entry:
            last_date = last_entry.execution_date
            return (now - last_date) / self.expected_period
        else:
            return 2137

    def execute(self, participant: User, date: Optional[datetime] = None):
        Execution.objects.create(
            execution_date=date, executed_by=participant, activity=self
        )


class Execution(models.Model):
    execution_date = models.DateTimeField("date done", auto_now_add=True)
    executed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

    def __str__(self, *args, **kwargs):
        return f"{self.activity.activity_name} done at {self.execution_date.strftime("%Y-%m-%d")} by {self.executed_by.first_name}"
