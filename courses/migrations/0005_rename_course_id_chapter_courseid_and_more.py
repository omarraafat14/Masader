# Generated by Django 4.1.3 on 2023-01-14 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_remove_chapter_course_remove_course_instructors_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chapter',
            old_name='course_id',
            new_name='courseID',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='instructor_id',
            new_name='instructorID',
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='videos',
        ),
        migrations.AddField(
            model_name='chapter',
            name='videoID',
            field=models.ManyToManyField(default=None, related_name='video', to='courses.video'),
        ),
    ]
