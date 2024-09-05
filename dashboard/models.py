from django.db import models

class Activity(models.Model):
    activity_name = models.CharField(max_length=200)
    date_created = models.DateTimeField("date created", auto_now_add=True)
    expected_period = models.DurationField("expected period")

class Participant(models.Model):
    participant_name = models.CharField(max_length=200)

class Execution(models.Model):
    execution_date = models.DateTimeField("date done")
    executed_by = models.ForeignKey(Participant, on_delete = models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete = models.CASCADE)


