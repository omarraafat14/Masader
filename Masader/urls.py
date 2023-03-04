"""Masader URL Configuration"""

from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls')),
    path('api/' , include('courses.urls')),
    path('cart/' , include('cart.urls')),
    path('users/' , include('users.urls')),
    path('orders/' , include('orders.urls')),
    
    # User registration and token generation endpoints
    path('auth/', include('djoser.urls')),
    # Include Token-Based Login
    path('token/', include('djoser.urls.authtoken')),
]

handler404 = "Masader.views.handler404"