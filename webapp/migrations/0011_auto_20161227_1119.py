# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-27 11:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0010_auto_20161227_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='head',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='webapp.Student'),
        ),
    ]
