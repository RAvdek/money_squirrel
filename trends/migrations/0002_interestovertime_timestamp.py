# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-15 00:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trends', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='interestovertime',
            name='timestamp',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]