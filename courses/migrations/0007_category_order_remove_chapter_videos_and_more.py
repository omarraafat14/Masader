# Generated by Django 4.1.3 on 2023-02-05 15:17

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0006_remove_chapter_courseid_remove_chapter_videoid_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=255)),
                ('slug', models.SlugField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(db_index=True, default=0)),
                ('total', models.DecimalField(decimal_places=2, max_digits=6)),
                ('date', models.DateField(auto_now_add=True, db_index=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='videos',
        ),
        migrations.RemoveField(
            model_name='course',
            name='description',
        ),
        migrations.RemoveField(
            model_name='course',
            name='instructors',
        ),
        migrations.RemoveField(
            model_name='course',
            name='name',
        ),
        migrations.RemoveField(
            model_name='course',
            name='overview',
        ),
        migrations.RemoveField(
            model_name='course',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='instructor',
            name='rating',
        ),
        migrations.AddField(
            model_name='course',
            name='title',
            field=models.CharField(db_index=True, default='Lorem ipsum', max_length=255),
        ),
        migrations.AddField(
            model_name='instructor',
            name='course',
            field=models.ManyToManyField(blank=True, to='courses.course'),
        ),
        migrations.AddField(
            model_name='video',
            name='chapter',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='courses.chapter'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='course',
            name='language',
            field=models.CharField(default='English', max_length=200),
        ),
        migrations.AlterField(
            model_name='course',
            name='price',
            field=models.DecimalField(db_index=True, decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='course',
            name='subtitle',
            field=models.CharField(default='English', max_length=200),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='name',
            field=models.CharField(db_index=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='video',
            name='summary',
            field=models.CharField(default='summary', max_length=255),
        ),
        migrations.AlterField(
            model_name='video',
            name='title',
            field=models.CharField(db_index=True, max_length=25),
        ),
        migrations.AlterField(
            model_name='course',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='courses.category'),
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.DecimalField(decimal_places=1, default=2.5, max_digits=2, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(5.0)])),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'course')},
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.order')),
            ],
            options={
                'unique_together': {('order', 'course')},
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('course', 'user')},
            },
        ),
    ]
