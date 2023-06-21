from dataclasses import field
from django.shortcuts import render
from .models import Building, Course, Department
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
import pandas as pd
from io import BytesIO
from django.http import FileResponse
from exam.models import Exam
from .forms import ExamScheduleForm,DepartmentExportForm
from openpyxl import Workbook
from django.http import HttpResponse
from django_pandas.io import read_frame

class BuildingListView(ListView):
    model = Building
    context_object_name = 'buildings'
    ordering = ['building']


class BuildingDetailView(DetailView):
    model = Building


class DepartmentListView(View):
    def get(self, request):
        context = {}
        context['departments'] = Department.objects.all()
        return render(request, 'university/department_list.html', context)

    def post(self, request):
        pass


class DepartmentDetailView(DetailView):
    model = Department
    


def course_list(request):
    context = {}
    courses = Course.objects.all()
    context['courses'] = courses.order_by("course_name")
    if request.method == 'POST':
        order_method = request.POST['order_by']
        context['courses'] = courses.order_by(order_method)
    return render(request, 'university/course_list.html', context)

def export_exam_schedule(request):
    if request.method == 'POST':
        form = ExamScheduleForm(request.POST)
        if form.is_valid():
            classroom = form.cleaned_data['classroom']
            exams = Exam.objects.filter(location=classroom).order_by('start_date')

            data = []
            for exam in exams:
                invigilators = ', '.join([str(assignment.invigilator) for assignment in exam.invigilatorassignment_set.filter(assigned=True)])
                department = exam.course.department.department_name

                data.append({
                    'Ders Kodu':exam.course.course_code,
                    'Dil':exam.language_level,
                    'Öğretim Türü': dict(exam.EDUCATION_TYPE_CHOICES)[exam.education_type],
                    'Ders Adı': exam.course,
                    'Başlangıç Tarihi ve Saati': exam.start_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'Bitiş Tarihi ve Saati': exam.end_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'Gözetmen': invigilators,
                    'Bölüm': department,
                    'Sınav Türü': exam.unit,
                    
                    # ... diğer alanlar ...
                })
            df = pd.DataFrame(data)

            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)

            output.seek(0)

            response = FileResponse(output, as_attachment=True, filename=f'{classroom}_exam_schedule.xlsx')

            return response
    else:
        form = ExamScheduleForm()

    return render(request, 'your_template.html', {'form': form})

def export_department_exams(request):
    form = DepartmentExportForm()

    if request.method == "POST":
        form = DepartmentExportForm(request.POST)
        if form.is_valid():
            department = form.cleaned_data['department']
            
            exams = Exam.objects.filter(course__department=department).order_by('start_date')
            
            data = []
            for exam in exams:
                invigilators = ', '.join([str(assignment.invigilator) for assignment in exam.invigilatorassignment_set.filter(assigned=True)])
                locations = ', '.join([str(location) for location in exam.location.all()])
                data.append({
                    'Ders Kodu': exam.course.course_code,
                    'Dil': exam.language_level,
                    'Öğretim Türü': dict(exam.EDUCATION_TYPE_CHOICES)[exam.education_type],
                    'Ders Adı': exam.course,
                    'Başlangıç Tarihi ve Saati': exam.start_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'Bitiş Tarihi ve Saati': exam.end_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'Gözetmen': invigilators,
                    'Sınıf': locations,
                    'Sınav Türü': exam.unit,
                })
            df = pd.DataFrame(data)

            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)

            output.seek(0)

            response = FileResponse(output, as_attachment=True, filename=f'{department.department_name}_exams.xlsx')

            return response

    return render(request, 'export_department_exams.html', {'form': form})
