# Generated by Django 4.1.3 on 2022-12-11 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0012_course_instructors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='instructors',
            field=models.ManyToManyField(null=True, related_name='courses', to='courses.instructor'),
        ),
    ]
