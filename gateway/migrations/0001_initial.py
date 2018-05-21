# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-21 11:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gateway',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('action', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='GatewayState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=10)),
                ('task_name', models.CharField(max_length=20)),
                ('state', models.CharField(choices=[('P', 'Pass'), ('F', 'Fail')], max_length=1)),
                ('log', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]
