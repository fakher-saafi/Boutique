# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-14 09:25
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boutique1', '0005_auto_20170814_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 14, 10, 25, 36, 618226)),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 14, 10, 25, 36, 621217)),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 14, 10, 25, 36, 621217)),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 14, 10, 25, 36, 621217)),
        ),
    ]
