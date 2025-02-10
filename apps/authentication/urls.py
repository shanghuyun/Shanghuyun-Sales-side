# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, include

urlpatterns = [
    path('accounts/', include('allauth.urls')),
]