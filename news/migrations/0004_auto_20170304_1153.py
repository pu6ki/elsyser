# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-04 09:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_news_clazz'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='news',
            unique_together=set([]),
        ),
    ]