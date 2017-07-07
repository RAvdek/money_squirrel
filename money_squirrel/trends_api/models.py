# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class InterestByRegion(models.Model):

    geo = models.CharField(max_length=100)
    start_dt = models.DateTimeField()
    end_dt = models.DateTimeField()
    search_terms = models.CharField(max_length=200, default=None, blank=True, null=True)
    scores = JSONField()

    def __str__(self):
        return str({
            "geo": self.geo,
            "start_dt": self.start_dt,
            "end_dt": self.start_dt,
            "scores": self.scores,
            "search_terms": self.search_terms
        })


@python_2_unicode_compatible
class InterestOverTime(models.Model):

    geo = models.CharField(max_length=100, default=None, blank=True, null=True)
    dt = models.DateTimeField(default=None, blank=True, null=True)
    start_dt = models.DateTimeField()
    end_dt = models.DateTimeField()
    search_terms = models.CharField(max_length=200, default=None, blank=True, null=True)
    scores = JSONField()

    def __str__(self):
        return str({
            "geo": self.geo,
            "dt": self.dt,
            "start_dt": self.start_dt,
            "end_dt": self.end_dt,
            "scores": self.scores,
            "search_terms": self.search_terms
        })
