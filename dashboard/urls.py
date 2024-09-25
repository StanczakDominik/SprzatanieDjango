from django.urls import path
from django.conf import settings

from . import views

app_name = "dashboard"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("activity/<int:pk>/", views.DetailView.as_view(), name="detail"),
    # path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path(
        "activity/<int:activity_id>/do/",
        views.execute_activity,
        name="execute_activity",
    ),
    path("activity/create", views.ActivityCreateView.as_view(), name="create_activity"),
    path(
        "activity/<int:pk>/delete",
        views.ActivityDeleteView.as_view(),
        name="delete_activity",
    ),
    path(
        "activity/<int:pk>/update",
        views.ActivityUpdateView.as_view(),
        name="update_activity",
    ),
    path(
        "execution/create", views.ExecutionCreateView.as_view(), name="create_execution"
    ),
    path(
        "execution/<int:pk>/update",
        views.ExecutionUpdateView.as_view(),
        name="update_execution",
    ),
    path(
        "execution/<int:pk>/delete",
        views.ExecutionDeleteView.as_view(),
        name="delete_execution",
    ),
    path("yaml", views.upload_file, name="upload_yaml"),
]

if not settings.TESTING:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns = [
        *urlpatterns,
    ] + debug_toolbar_urls()
