# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'running/', TemplateView.as_view(template_name="session_info.html")),
    url(r'session/', views.start_session)
    ]
