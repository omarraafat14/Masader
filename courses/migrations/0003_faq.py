# Generated by Django 4.1.3 on 2023-01-08 01:33

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0002_video_summary_alter_video_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='The actual question itself.', verbose_name='question')),
                ('answer', models.TextField(blank=True, help_text='The answer text.', verbose_name='answer')),
                ('slug', models.SlugField(max_length=100, verbose_name='slug')),
                ('status', models.IntegerField(choices=[(1, 'Active'), (0, 'Inactive'), (2, 'Group Header')], default=0, help_text="Only questions with their status set to 'Active' will be displayed. Questions marked as 'Group Header' are treated as such by views and templates that are set up to use them.", verbose_name='status')),
                ('protected', models.BooleanField(default=False, help_text='Set true if this question is only visible by authenticated users.', verbose_name='is protected')),
                ('sort_order', models.IntegerField(default=0, help_text='The order you would like the question to be displayed.', verbose_name='sort order')),
                ('created_on', models.DateTimeField(default=datetime.datetime.now, verbose_name='created on')),
                ('updated_on', models.DateTimeField(verbose_name='updated on')),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='questions', to='courses.chapter', verbose_name='chapter')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='created by')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='updated by')),
            ],
            options={
                'verbose_name': 'Frequent asked question',
                'verbose_name_plural': 'Frequently asked questions',
                'ordering': ['sort_order', 'created_on'],
            },
        ),
    ]