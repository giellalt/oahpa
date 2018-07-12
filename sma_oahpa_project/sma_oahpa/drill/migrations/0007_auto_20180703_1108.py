# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-03 09:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drill', '0006_auto_20180702_1039'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='word',
            name='compsuffix',
        ),
        migrations.RemoveField(
            model_name='word',
            name='hom',
        ),
        migrations.AlterField(
            model_name='question',
            name='level',
            field=models.IntegerField(max_length=3),
        ),
        migrations.AlterField(
            model_name='word',
            name='hid',
            field=models.IntegerField(default=None, max_length=3, null=True),
        ),
    ]
