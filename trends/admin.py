# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import  InterestOverTime, InterestByRegion

# Register your models here.
admin.site.register(InterestOverTime)
admin.site.register(InterestByRegion)