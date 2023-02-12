from rest_framework import serializers
from .models import *
from rest_framework import status
from rest_framework.validators import UniqueValidator,UniqueTogetherValidator
from django.contrib.auth.password_validation import validate_password


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']


# Create Insreuctor Serializer 
class CourseSerializer(serializers.ModelSerializer):
  category = CategorySerializer(read_only=True)
  class Meta:
      model = Course
      fields = '__all__'


# Create Insreuctor Serializer 
class InstructorSerializer(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField()
    class Meta:
        model = Instructor
        fields =(
            'id', 'name', 'no_of_courses','courses',
        )

    def get_courses(self,obj):
        courses = obj.objects.all()
        return CourseSerializer(courses,many=True).data

# Serializer to get Chapter Details
class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Rating
        fields = ['user', 'course', 'rating']
        # validators = [UniqueTogetherValidator(queryset=Rating.objects.all(), fields=['user', 'course'])]
        # extra_kwargs = {
        #     'rating': {'min_value': 0, 'max_value': 5},
        # }



# Serializer to get Chapter Details
class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'


# Serializer to get Chapter Details
class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'

#Serializer to Get User Details using Django Token Authentication
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name','last_name', 'email'
        ]



class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        # fields = ['id','user', 'course','course_price', 'total_price']
        exclude = ['user']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields= '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    cart = CartSerializer()
    class Meta:
        model = OrderItem
        fields = ['order','course','cart']
        
