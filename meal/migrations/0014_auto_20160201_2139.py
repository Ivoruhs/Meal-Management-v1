# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-01 15:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meal', '0013_auto_20160201_2134'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='flog',
            new_name='Log',
        ),
    ]