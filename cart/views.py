from rest_framework import generics, status
from .serializers import CartSerializer, CartItemSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from .models import Cart, CartItem
from courses.permissions import *
from django.shortcuts import get_object_or_404
from courses.models import Course


# Create your views here.
class CartView(generics.RetrieveUpdateAPIView):
    """represent a single model instance."""
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        """Returns an object instance that should be used for detail views."""
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart
    

class AddToCartView(generics.CreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsStudent]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *arg, **kwargs):
        course_id = request.data.get('course')
        course = get_object_or_404(Course, id=course_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, course=course)
        cart_item.save()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

    def delete(self, request, *arg, **kwargs):
        if request.data['course']:
            serialized_item = CartSerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            course = request.data['course']
            cart = get_object_or_404(Cart, user=request.user, course=course )
            cart.delete()
            return Response(status=status.HTTP_200_OK, data={'message':'course removed from cart'})
        else:
            Cart.objects.filter(user=request.user).delete()
            return Response(status=status.HTTP_201_CREATED, data={'message':'All courses removed from cart'})