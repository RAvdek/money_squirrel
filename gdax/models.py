# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class GDAXPrice(models.Model):

    product = models.CharField(max_length=10)
    granularity = models.IntegerField()
    dt = models.DateTimeField()
    low = models.FloatField()
    high = models.FloatField()
    open = models.FloatField()
    close = models.FloatField()
    volume = models.FloatField()

    def __str__(self):
        return str({
            "product": self.product,
            "granularity": self.granularity,
            "dt": self.dt,
            "low": self.low,
            "high": self.high,
            "open": self.open,
            "close": self.close,
            "volume": self.volume,
        })