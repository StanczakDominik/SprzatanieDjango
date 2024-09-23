from .models import Activity, Execution

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = "dashboard/index.html"
    context_object_name = "activities"

    def get_queryset(self):
        return Activity.objects.order_by("-date_created")


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Activity
    template_name = "dashboard/detail.html"


@login_required
def execute_activity(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    execution = Execution(executed_by=request.user, activity=activity)
    execution.save()
    return HttpResponseRedirect(reverse_lazy("dashboard:detail", args=[activity_id]))

class ActivityCreateView(LoginRequiredMixin, generic.CreateView):
    model = Activity
    fields = ["activity_name", "expected_period"]
    success_url = reverse_lazy("dashboard:index")

