# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-26 18:55
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meal', '0002_auto_20160125_2326'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dep_name', models.CharField(max_length=20)),
                ('location', models.CharField(max_length=10)),
            ],
        ),
        migrations.AlterField(
            model_name='meallog',
            name='date',
            field=models.DateField(default=datetime.datetime(2016, 1, 26, 18, 55, 11, 364249)),
        ),
    ]
