# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-06-03 06:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_comment_author_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='clazz',
        ),
        migrations.AddField(
            model_name='news',
            name='class_letter',
            field=models.CharField(blank=True, max_length=1),
        ),
        migrations.AddField(
            model_name='news',
            name='class_number',
            field=models.IntegerField(default=8),
        ),
    ]
