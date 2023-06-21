# Generated by Django 4.0.4 on 2022-06-03 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('exam', '0001_initial'),
        ('university', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exams', to='university.course'),
        ),
        migrations.AddField(
            model_name='exam',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='exams', to='university.classroom'),
        ),
        migrations.AddField(
            model_name='exam',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exams', to='university.unit'),
        ),
    ]