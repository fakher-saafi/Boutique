# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-27 19:09
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boutique1', '0019_auto_20170827_1855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 27, 19, 9, 42, 882313)),
        ),
        migrations.AlterUniqueTogether(
            name='promotion',
            unique_together=set([]),
        ),
    ]
