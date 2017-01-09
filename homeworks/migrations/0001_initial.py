# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-09 14:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deadline', models.DateField()),
                ('details', models.TextField(blank=True, max_length=256)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='students.Teacher')),
                ('clazz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.Class')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.Subject')),
            ],
            options={
                'ordering': ['-deadline', 'clazz', 'subject'],
            },
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=2048)),
                ('solution_url', models.URLField(blank=True)),
                ('posted_on', models.DateTimeField(auto_now_add=True)),
                ('edited', models.BooleanField(default=False)),
                ('last_edited_on', models.DateTimeField(auto_now=True)),
                ('checked', models.BooleanField(default=False)),
                ('homework', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homeworks.Homework')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.Student')),
            ],
            options={
                'ordering': ['-posted_on', '-last_edited_on'],
            },
        ),
    ]
