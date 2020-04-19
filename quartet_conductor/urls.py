# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView

from quartet_conductor import views
from quartet_conductor.routers import urlpatterns as api_patterns
urlpatterns = [
    url(r'^running/?$', views.session_info),
    url(r'^session/?$', views.start_session),
    url(r'^input_maps/?$', views.InputMapView.as_view()),
    path('input-map/<int:id>/', views.input_map_detail)
    ]
urlpatterns += api_patterns


