from django.db import models
from university.models import Course, Unit, Classroom
from datetime import timedelta
from django.core.exceptions import ValidationError
# Create your models here.

class Invigilator(models.Model):
    name = models.CharField(max_length=200)
    availability = models.ManyToManyField('Exam', through='InvigilatorAssignment')

    def __str__(self):
        return self.name

class InvigilatorAssignment(models.Model):
    exam = models.ForeignKey('Exam', on_delete=models.CASCADE)
    invigilator = models.ForeignKey('Invigilator', on_delete=models.CASCADE)
    assigned = models.BooleanField(default=False)

    def clean(self):
        conflicting_exams = Exam.objects.filter(
            start_date=self.exam.start_date,
            invigilatorassignment__assigned=True,
            invigilatorassignment__invigilator=self.invigilator
        ).exclude(invigilatorassignment=self)

        if conflicting_exams.exists():
            raise ValidationError('Bu gözetmenin aynı saat ve tarihte başka bir sınavı var.')

    class Meta:
        unique_together = ('exam', 'invigilator')



class Exam(models.Model):
    ENGLISH_LEVEL_CHOICES = [
        ('0', '0% English'),
        ('30', '30% English'),
        ('100', '100% English'),
    ]
    language_level = models.CharField(max_length=3, choices=ENGLISH_LEVEL_CHOICES, default='0')
    EXAM_TYPE_CHOICES = [('Midterm', 'Midterm',), ('Final', 'Final',), ('Make-up', 'Make-up',)]
    exam_type = models.CharField(max_length=50, choices=EXAM_TYPE_CHOICES)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="exams")
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="exams")
    start_date = models.DateTimeField()
    duration = models.IntegerField(null=True)
    end_date = models.DateTimeField(blank=True, null=True, editable=False)
    location = models.ManyToManyField(Classroom, related_name="exams")
    EDUCATION_TYPE_CHOICES = [('1', '1. Öğretim'), ('2', '2. Öğretim'),]
    education_type = models.CharField(max_length=1, choices=EDUCATION_TYPE_CHOICES, default='1')

    def __str__(self):
        return self.course.course_name

    def save(self, *args, **kwargs):
        same_type_exam_exists = Exam.objects.filter(
            course=self.course, exam_type=self.exam_type, unit=self.unit,
            education_type=self.education_type, language_level=self.language_level
        ).exclude(pk=self.pk).exists()

        if same_type_exam_exists:
            raise ValidationError('Bu ders için zaten aynı tip ve eğitim türünde bir sınav bulunmaktadır.')

        same_department_exam_exists = Exam.objects.filter(
            course__department=self.course.department, start_date=self.start_date,
        ).exclude(course=self.course).exists()

        if same_department_exam_exists:
            raise ValidationError('Aynı bölüme, aynı saat ve tarihte başka bir sınav bulunmaktadır.')

        super().save(*args, **kwargs)

        self.end_date = self.start_date + timedelta(minutes=self.duration)
        self.class_size = sum([location.capacity for location in self.location.all()])

        try:
            for location in self.location.all():
                conflicting_exams = Exam.objects.filter(
                    location=location,
                    start_date__lte=self.end_date,
                    end_date__gte=self.start_date
                ).exclude(pk=self.pk)

                if conflicting_exams.exists():
                    raise ValidationError(f'{location} sınıfında o saat ve tarihte bir sınav bulunmaktadır.')
        except ValidationError:
            self.delete()
            raise

        super().save(*args, **kwargs)




    class Meta:
        models.UniqueConstraint(
            fields=['start_date', 'location'], name="Date and Location")
        models.UniqueConstraint(fields=['course', 'exam_type', 'unit'], name="Course, Type, Unit")