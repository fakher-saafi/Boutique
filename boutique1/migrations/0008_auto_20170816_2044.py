# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-16 19:44
from __future__ import unicode_literals

import boutique1.models
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boutique1', '0007_auto_20170814_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 16, 20, 44, 39, 947211)),
        ),
        migrations.AlterField(
            model_name='collection',
            name='image_collection',
            field=models.ImageField(blank=True, null=True, upload_to=boutique1.models.user_directory_path_five),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='collection',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='boutique1.Collection'),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 16, 20, 44, 39, 950210)),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 16, 20, 44, 39, 950711)),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='produit',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='boutique1.Produit'),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='promotion_type',
            field=models.CharField(blank=True, choices=[('RE', 'Regular'), ('FL', 'Flash')], max_length=20),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 16, 20, 44, 39, 950711)),
        ),
    ]
