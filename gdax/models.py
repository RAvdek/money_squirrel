# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class GDAXPrice(models.Model):

    product = models.CharField(max_length=10)
    interval = models.IntegerField()
    dt = models.DateTimeField()
    low = models.FloatField()
    high = models.FloatField()
    open = models.FloatField()
    close = models.FloatField()
    volume = models.FloatField()
