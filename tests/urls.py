# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include

from quartet_conductor.urls import urlpatterns as quartet_conductor_urls

app_name = 'quartet_conductor'

urlpatterns = [
    url(r'^', include(quartet_conductor_urls)),
]
