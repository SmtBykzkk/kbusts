from django.contrib import admin
from .models import Exam, Invigilator, InvigilatorAssignment

class ExamAdmin(admin.ModelAdmin):
    list_display = ("exam_type", "course", "unit", "start_date", "get_locations")
    readonly_fields = ("id",)

    def get_locations(self, obj):
        return ", ".join([str(location) for location in obj.location.all()])
    get_locations.short_description = 'Sınıflar'

admin.site.register(Exam, ExamAdmin)
admin.site.register(InvigilatorAssignment)
admin.site.register(Invigilator)
