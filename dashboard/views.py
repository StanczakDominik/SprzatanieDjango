from django.shortcuts import render

from .models import Activity, Participant, Execution

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import generic


class IndexView(generic.ListView):
    template_name = "dashboard/index.html"
    context_object_name = "activities"

    def get_queryset(self):
        return Activity.objects.order_by("-date_created")


class DetailView(generic.DetailView):
    model = Activity
    template_name = "dashboard/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["participants"] = Participant.objects.all()
        return context


def do(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    try:
        participant = Participant.objects.get(pk=request.POST["participant"])
    except (KeyError, Participant.DoesNotExist):
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
