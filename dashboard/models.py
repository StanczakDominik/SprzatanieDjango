from django.db import models
from django.db.models.query import QuerySet
from datetime import date
from django.contrib.auth.models import User
import humanize


class Activity(models.Model):
    activity_name = models.CharField(max_length=200)
    date_created = models.DateField("date created", default=date.today, null=False)
    expected_period = models.DurationField("expected period")
    notes = models.TextField(
        "Notes or description of the activity", default="", blank=True
    )

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

    def execute(self, participant: User | list[User]):
        ex = Execution.objects.create(activity=self)
        if not isinstance(participant, QuerySet):
            participant = [participant]
        for p in participant:
            ex.executed_by.add(p)
        ex.save()


class Execution(models.Model):
    execution_date = models.DateField("date done", default=date.today)
    executed_by = models.ManyToManyField(User, blank=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

    def __str__(self, *args, **kwargs):
        output = f"{self.activity.activity_name} done at {self.execution_date.strftime('%Y-%m-%d')}"
        if users := self.executed_by.all():
            output += " by " + humanize.natural_list(
                [
                    user.first_name if user.first_name else user.username
                    for user in users
                ]
            )
        return output
