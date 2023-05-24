from django.contrib import admin
from .models import Employee,Schedule, WeeklyShiftPlan, CalenderWeek, Preferences
# Register your models here.

admin.site.register(Employee)
admin.site.register(Schedule)
admin.site.register(WeeklyShiftPlan)
admin.site.register(CalenderWeek)
admin.site.register(Preferences)