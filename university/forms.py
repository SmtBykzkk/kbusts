from django import forms
from .models import Classroom
from .models import Department

class ExamScheduleForm(forms.Form):
    classroom = forms.ModelChoiceField(queryset=Classroom.objects.all())

class DepartmentExportForm(forms.Form):
    department = forms.ModelChoiceField(queryset=Department.objects.all()) 