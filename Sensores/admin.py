from django.contrib import admin
from .models import SensorStats, FailureLogs

admin.site.register(SensorStats)
admin.site.register(FailureLogs)
