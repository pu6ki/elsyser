# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-09-19 19:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homeworks', '0002_homework_topic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homework',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='homeworks', to='students.Teacher'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='homework',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='homeworks.Homework'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='students.Student'),
        ),
    ]
