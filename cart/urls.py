from django.urls import path
from . import views

urlpatterns = [
    path('cart-detail/', views.CartView.as_view(), name='cart-detail'),
    path('add-to-cart/', views.AddToCartView.as_view(), name='add-to-cart'),
]