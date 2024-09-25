from django.db import models
from datetime import date
from django.contrib.auth.models import User


class Activity(models.Model):
    activity_name = models.CharField(max_length=200)
    date_created = models.DateField("date created", default=date.today, null=False)
    expected_period = models.DurationField("expected period")

    @property
    def last_entry(self):
        try:
            return self.associated_executions_by_date[0]
        except IndexError:
            return None

    def __str__(self, *args, **kwargs):
        return self.activity_name

    @property
    def priority(self):
        now = date.today()

        last_entry = self.last_entry

        if last_entry:
            last_date = last_entry.execution_date
        else:
            last_date = self.date_created
        return (now - last_date) / self.expected_period

    @property
    def associated_executions_by_date(self):
        return self.execution_set.order_by("-execution_date")

    def execute(self, participant: User):
        Execution.objects.create(executed_by=participant, activity=self)


class Execution(models.Model):
    execution_date = models.DateField("date done", default=date.today)
    executed_by = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True
    )
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

    def __str__(self, *args, **kwargs):
        output = f"{self.activity.activity_name} done at {self.execution_date.strftime("%Y-%m-%d")}"
        if self.executed_by is None:
            by = ""
        elif self.executed_by.first_name:
            by = f" by {self.executed_by.first_name}"
        else:
            f" by {self.executed_by.nickname}"
        return output + by
