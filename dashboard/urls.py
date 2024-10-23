from django.urls import path

from . import views

app_name = "dashboard"
urlpatterns = [
    path("<slug:slug>", views.IndexView.as_view(), name="index"),
    path("activity/<int:pk>/", views.DetailView.as_view(), name="detail"),
    # path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path(
        "activity/<int:activity_id>/do/",
        views.execute_activity,
        name="execute_activity",
    ),
    path(
        "activity/<int:activity_id>/do_as_team/",
        views.execute_activity_team,
        name="execute_activity_team",
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
        "execution/create/<int:pk>",
        views.ExecutionCreateView.as_view(),
        name="create_execution",
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
