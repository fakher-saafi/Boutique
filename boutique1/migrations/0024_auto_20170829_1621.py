# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-29 16:21
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boutique1', '0023_auto_20170829_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 29, 16, 21, 13, 569859)),
        ),
    ]