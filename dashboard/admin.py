from django.contrib import admin

from .models import Activity, Execution, Dashboard

admin.site.register(Activity)
admin.site.register(Execution)
admin.site.register(Dashboard)
