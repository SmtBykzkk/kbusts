# Generated by Django 4.1.7 on 2023-05-22 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructor', '0006_alter_instructor_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructor',
            name='profile_image',
            field=models.ImageField(blank=True, default='/default_images/default_profile.png', null=True, upload_to='profile_images'),
        ),
    ]
