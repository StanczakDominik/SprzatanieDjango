from django.shortcuts import render

from .models import Activity, Execution

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import generic
from django.contrib.auth.models import User


class IndexView(generic.ListView):
    template_name = "dashboard/index.html"
    context_object_name = "activities"

    def get_queryset(self):
        return Activity.objects.order_by("-date_created")


class DetailView(generic.DetailView):
    model = Activity
    template_name = "dashboard/detail.html"

def execute_activity(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    try:
        participant = User.objects.get(pk=request.POST["participant"])
    except (KeyError, User.DoesNotExist):
        return render(
            request,
            "dashboard/detail.html",
            {
                "error_message": "You didn't select a participant.",
            },
        )
    else:
        execution = Execution(executed_by=participant, activity=activity)
        execution.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(f"/dashboard/{activity_id}")
