from django.urls import path
from .views import (
    CreateOrderView,
    OrderListView,
)


urlpatterns = [
    path('create-order/', CreateOrderView.as_view(), name='create-order'),
    path('order-list/', OrderListView.as_view(), name='order-list'),
]