# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-02 08:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drill', '0003_form_dialects'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='level',
            field=models.IntegerField(default=1),
        ),
    ]
