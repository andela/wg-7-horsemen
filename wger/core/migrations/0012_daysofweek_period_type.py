# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-12-10 09:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_apiuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='daysofweek',
            name='period_type',
            field=models.CharField(blank=True, max_length=9, null=True),
        ),
    ]
