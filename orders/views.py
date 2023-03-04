from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.response import Response
from rest_framework import generics
from cart.models import Cart, CartItem
from courses.permissions import *


# Create your views here.
class CreateOrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsStudent]
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle,AnonRateThrottle]

    def post(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, user=request.user)
        order = Order(user=request.user, total=0)
        order.save()
        order_items = []
        total = 0
        for cart_item in cart.items.all():
            order_item = OrderItem(
                order=order,
                course=cart_item.course,
            )
            order_items.append(order_item)
            total += order_item.course.price
        order.total = total
        order.save()
        OrderItem.objects.bulk_create(order_items)  # creates multiple objects of the OrderItem in a snigle query
        cart.items.all().delete()
        serializer = OrderSerializer(order)
        return Response(serializer.data)


class DeleteOrderView(generics.UpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsStudent]
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle,AnonRateThrottle]

    def delete(self, request, *args, **kwargs):
        order = Order.objects.get(pk=self.kwargs['pk'])
        order_number = str(order.id)
        order.delete()
        return Response(status=200, data={'message':'Order #{} was deleted'.format(order_number)})


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    # queryset = OrderItem.objects.all()
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle,AnonRateThrottle]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Student').exists():
            return Order.objects.all().filter(user = user)
        elif user.groups.filter(name='Instructor').exists():
            return Order.objects.all().filter(user = user)
        else:
            return Order.objects.all()