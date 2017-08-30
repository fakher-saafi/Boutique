# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-14 09:25
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boutique1', '0004_auto_20170810_1107'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000)),
                ('description', models.CharField(max_length=1000)),
                ('is_active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2017, 8, 14, 10, 25, 14, 647335))),
                ('owner', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='boutique1.Trader')),
            ],
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=datetime.datetime(2017, 8, 14, 10, 25, 14, 649338))),
                ('status', models.BooleanField(default=False)),
                ('start_time', models.DateTimeField(default=datetime.datetime(2017, 8, 14, 10, 25, 14, 649338))),
                ('end_time', models.DateTimeField(default=datetime.datetime(2017, 8, 14, 10, 25, 14, 649338))),
                ('discount_value', models.IntegerField(default=0)),
                ('promotion_type', models.CharField(blank=True, choices=[('HM', 'Regular'), ('VTG', 'Flash')], max_length=20)),
                ('promotion_for', models.CharField(blank=True, choices=[('PR', 'Product'), ('CO', 'Collection')], max_length=20)),
                ('collection', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='boutique1.Collection')),
            ],
        ),
        migrations.AlterField(
            model_name='produit',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='promotion',
            name='produit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boutique1.Produit'),
        ),
        migrations.AddField(
            model_name='collection',
            name='produit',
            field=models.ManyToManyField(default=1, to='boutique1.Produit'),
        ),
    ]
