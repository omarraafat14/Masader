from rest_framework import serializers
from .models import *
from courses.serializers import CourseSerializer


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for the CartItem model."""
    course = CourseSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'course']


class CartSerializer(serializers.ModelSerializer):
    """Serializer for the Cart model."""
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items']
