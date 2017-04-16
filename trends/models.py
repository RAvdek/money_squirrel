# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.


class InterestByRegion(models.Model):

    geo_name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    scores = JSONField()


class InterestOverTime(models.Model):

    geo_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    dt = models.DateTimeField(default=None, blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    scores = JSONField()

