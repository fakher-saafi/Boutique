# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-27 18:55
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boutique1', '0018_auto_20170825_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 27, 18, 55, 38, 264957)),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='collection',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='boutique1.Collection'),
        ),
        migrations.AlterUniqueTogether(
            name='promotion',
            unique_together=set([('produit', 'is_active')]),
        ),
    ]