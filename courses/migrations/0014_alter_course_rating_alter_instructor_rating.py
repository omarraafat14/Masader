# Generated by Django 4.1.3 on 2022-12-16 14:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0013_alter_course_instructors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=4.5, max_digits=2, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(5.0)]),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=4.0, max_digits=2, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(5.0)]),
        ),
    ]
