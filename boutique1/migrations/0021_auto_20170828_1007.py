# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-28 10:07
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boutique1', '0020_auto_20170827_1909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 28, 10, 7, 38, 193577)),
        ),
    ]