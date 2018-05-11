# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-11 22:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='OHLCV',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=10)),
                ('code', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=50)),
                ('open_price', models.IntegerField()),
                ('high_price', models.IntegerField()),
                ('low_price', models.IntegerField()),
                ('close_price', models.IntegerField()),
                ('adj_close_price', models.IntegerField(blank=True, null=True)),
                ('volume', models.IntegerField()),
                ('short_volume', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ticker',
            fields=[
                ('date', models.CharField(max_length=10)),
                ('code', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('market_type', models.CharField(max_length=10)),
                ('state', models.BooleanField(default=True)),
            ],
        ),
    ]