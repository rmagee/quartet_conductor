# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import TemplateView

from quartet_conductor import views

urlpatterns = [
    url(r'^running/?$', views.session_info),
    url(r'^session/?$', views.start_session)
    ]
