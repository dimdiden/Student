# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-27 12:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0012_auto_20161227_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='head',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='webapp.Student'),
        ),
    ]