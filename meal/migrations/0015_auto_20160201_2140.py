# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-01 15:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meal', '0014_auto_20160201_2139'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Log',
            new_name='Flog',
        ),
    ]
