# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-15 10:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_group_parent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='parent',
            new_name='head',
        ),
    ]
