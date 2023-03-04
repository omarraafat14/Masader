from rest_framework import serializers
from .models import *
from rest_framework import status
from courses.serializers import CourseSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for the OrderItem model."""
    course = CourseSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'course']


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for the Order model."""
    orders = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'total', 'created_at', 'orders']
