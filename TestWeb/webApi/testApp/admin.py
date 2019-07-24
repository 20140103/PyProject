# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from testApp.models import Topic
from testApp.models import Entry
# Register your models here.
admin.site.register(Topic)
admin.site.register(Entry) 