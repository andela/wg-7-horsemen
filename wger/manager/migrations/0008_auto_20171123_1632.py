# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-11-23 13:32
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0007_auto_20160311_2258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='reps',
            field=models.IntegerField(
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(600)],
                verbose_name='Amount'),
        ),
    ]
