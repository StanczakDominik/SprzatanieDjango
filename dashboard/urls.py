from django.urls import path
from django.conf import settings

from . import views

app_name = "dashboard"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("activity/<int:pk>/", views.DetailView.as_view(), name="detail"),
    # path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("activity/<int:activity_id>/do/", views.execute_activity, name="execute_activity"),
    path("activity/create", views.ActivityCreateView.as_view(), name="create_activity"),
]

if not settings.TESTING:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns = [
        *urlpatterns,
    ] + debug_toolbar_urls()
