# Generated by Django 4.0.4 on 2022-06-06 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructor', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructor',
            name='profile_image',
            field=models.ImageField(blank=True, default='/user_media/default_images/default_profile.png', null=True, upload_to='profile_images'),
        ),
    ]