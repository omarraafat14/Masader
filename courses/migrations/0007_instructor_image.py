# Generated by Django 4.1.3 on 2022-12-11 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_remove_instructor_courses_instructor_courses'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructor',
            name='image',
            field=models.ImageField(default='avatar.png', upload_to='images\\instructors'),
        ),
    ]