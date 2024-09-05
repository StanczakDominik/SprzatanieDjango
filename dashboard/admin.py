from django.contrib import admin

from .models import Activity, Participant, Execution

admin.site.register(Activity)
admin.site.register(Participant)
admin.site.register(Execution)
