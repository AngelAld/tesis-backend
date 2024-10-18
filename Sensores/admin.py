from django.contrib import admin
from .models import SensorStats, FailureLogs, DataSet

admin.site.register(SensorStats)
admin.site.register(FailureLogs)
admin.site.register(DataSet)
