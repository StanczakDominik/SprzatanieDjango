from .models import Activity, Execution
from datetime import timedelta

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from .forms import UploadFileForm
import yaml


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = "dashboard/index.html"
    context_object_name = "activities"

    @property
    def cutoff(self):
        try:
            cutoff = float(self.request.GET.get("priority", 1))
        except ValueError:
            cutoff = 1.0
        return cutoff

    def get_queryset(self):
        activities = Activity.objects.order_by("-date_created")
        activities = list(
            filter(lambda activity: activity.priority >= self.cutoff, activities)
        )
        activities = sorted(
            activities, key=lambda activity: activity.priority, reverse=True
        )
        return activities

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["priority"] = self.cutoff
        return context


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Activity
    template_name = "dashboard/detail.html"


@login_required
def execute_activity(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    activity.execute(request.user)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


class ActivityCreateView(LoginRequiredMixin, generic.CreateView):
    model = Activity
    fields = ["activity_name", "expected_period", "notes"]
    success_url = reverse_lazy("dashboard:index")


class ActivityUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Activity
    fields = ["activity_name", "expected_period", "notes"]

    def get_success_url(self):
        return reverse("dashboard:detail", args=[self.object.id])


class ActivityDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Activity
    # fields = ["activity_name", "expected_period", "notes"]

    def get_success_url(self):
        return reverse("dashboard:index")


class ExecutionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Execution
    # fields = ["executed_by"]

    def get_success_url(self):
        return reverse("dashboard:detail", args=[self.object.activity.id])


class ExecutionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Execution
    fields = ["executed_by", "execution_date"]

    def get_success_url(self):
        return reverse("dashboard:detail", args=[self.object.activity.id])


def parse_period(period):
    if period.endswith("w"):
        return timedelta(days=7 * int(period.strip("w")))
    elif period.endswith("d"):
        return timedelta(days=int(period.strip("d")))
    else:
        raise ValueError(f"Period must be d for days or w for weeks and not `{period}`")


def handle_uploaded_file(f):
    d = yaml.load(f, Loader=yaml.FullLoader)
    for activity_name, activity_dict in d.items():
        activity_period = parse_period(activity_dict["period"])
        if existing_activities := Activity.objects.filter(
            activity_name=activity_name,
        ):
            activity = existing_activities.get()
            if activity.expected_period != activity_period:
                raise ValueError(
                    f"Mismatch on expected period of {activity.activity_name}"
                )  # TODO how to handle this, actually?
        else:
            activity = Activity(
                activity_name=activity_name, expected_period=activity_period
            )
            activity.save()

        executions = []
        for date in activity_dict["dates"]:
            if not Execution.objects.filter(activity=activity, execution_date=date):
                execution = Execution(
                    execution_date=date,
                    activity=activity,
                )
                executions.append(execution)

        Execution.objects.bulk_create(executions)


def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES["file"])
            return HttpResponseRedirect(reverse("dashboard:index"))
    else:
        form = UploadFileForm()
    return render(request, "dashboard/upload.html", {"form": form})
