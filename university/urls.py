from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from .views import export_department_exams
urlpatterns = [
    path('building-list', login_required(views.BuildingListView.as_view()), name='building-list'),
    path('department-list', login_required(views.DepartmentListView.as_view()), name='department-list'),
    path('course-list', login_required(views.course_list), name='course-list'),
    path('building-detail/<slug:slug>', login_required(views.BuildingDetailView.as_view()), name='building-detail'),
    path('department-detail/<slug:slug>', login_required(views.DepartmentDetailView.as_view()), name='department-detail'),
    path('export_exam_schedule/', views.export_exam_schedule, name='export_exam_schedule'),
    path('export_department_exams/', export_department_exams, name='export_department_exams'),
]