# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-07 17:05
from __future__ import unicode_literals

from django.db import migrations, models
import students.models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0020_homework_materials'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homework',
            name='materials',
            field=models.FileField(blank=True, null=True, upload_to=students.models.homework_material_filename),
        ),
    ]