from django.contrib import admin
from .models import Record, Schedule, Vaccine, Immunogen

class RecordAdmin(admin.ModelAdmin):
    list_display = ('id','first_name','last_name', 'birth_date', 'parent_name','parent_mobile','home_address', 'weight','height' )

admin.site.register(Record, RecordAdmin)

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('vaccine_type',)


admin.site.register(Schedule, ScheduleAdmin)


class VaccineAdmin(admin.ModelAdmin):
    list_display = ('timing',)

admin.site.register(Vaccine, VaccineAdmin)
admin.site.register(Immunogen)
