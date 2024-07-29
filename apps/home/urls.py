# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('seller/<int:id>/', views.seller_detail_view, name='seller_detail'),
    path('api/products/<int:seller_id>/', views.product_list, name='product_list'),
    path('api/productsImages/<int:product_id>/', views.product_photos, name='product_photos'),
    # Matches any html file
    re_path(r'^.*\.html$', views.pages, name='pages'),
]