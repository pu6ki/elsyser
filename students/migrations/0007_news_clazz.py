# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-05 07:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0006_auto_20161105_0931'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='clazz',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='students.Class'),
            preserve_default=False,
        ),
    ]
