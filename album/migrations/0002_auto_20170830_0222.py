# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-30 02:22
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 30, 2, 22, 21, 963863)),
        ),
        migrations.AlterField(
            model_name='picture',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 30, 2, 22, 21, 964874)),
        ),
    ]
