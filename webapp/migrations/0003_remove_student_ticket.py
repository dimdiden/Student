# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-14 16:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_auto_20161214_1557'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='ticket',
        ),
    ]