from django.contrib import admin
from django.contrib.auth.models import Permission

from .models import Activity, Dashboard, Execution


class DashboardPermission(Permission):
    name = "Dashboard Permission"
    verbose_name = "View dashboard"


admin.site.register(Activity)
admin.site.register(Execution)
admin.site.register(Dashboard)
admin.site.register(DashboardPermission)
