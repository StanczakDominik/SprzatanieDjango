from django.shortcuts import render

from .models import Activity

def index(request):
    activities = Activity.objects.order_by("-date_created")
    context = {"activities": activities}
    return render(request, "dashboard/index.html", context)
