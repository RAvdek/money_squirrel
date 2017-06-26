# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Quote(models.Model):

    product_id = models.CharField(max_length=20)
    granularity = models.IntegerField()
    dt = models.DateTimeField()
    low = models.FloatField()
    high = models.FloatField()
    open = models.FloatField()
    close = models.FloatField()
    volume = models.FloatField()

    def __str__(self):
        return str({
            "product_id": self.product_id,
            "granularity": self.granularity,
            "dt": self.dt,
            "low": self.low,
            "high": self.high,
            "open": self.open,
            "close": self.close,
            "volume": self.volume,
        })
