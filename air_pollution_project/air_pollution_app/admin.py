from django.contrib import admin
from .models import AirPollutionDataItem, SomeData
# Register your models here.

admin.site.register(AirPollutionDataItem)
admin.site.register(SomeData)