# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class InterestByRegion(models.Model):

    geo_name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    scores = JSONField()

    def __str__(self):
        return str({
            "geo_name": self.geo_name,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "scores": self.scores,
        })


@python_2_unicode_compatible
class InterestOverTime(models.Model):

    geo_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    dt = models.DateTimeField(default=None, blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    scores = JSONField()

    def __str__(self):
        return str({
            "geo_name": self.geo_name,
            "dt": self.dt,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "scores": self.scores,
        })
