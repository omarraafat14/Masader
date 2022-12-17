from django.shortcuts import render
from rest_framework import generics , mixins , viewsets 
from .models import *
from .serializers import *
from rest_framework import filters
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication

# Create Viewsets endpoint
class viewsete_courses(viewsets.ModelViewSet):
    queryset = Course.objects.all()    
    serializer_class = CourseSerializer
    filter_backend = [filters.SearchFilter]
    search_field = ['name']  

class InstructorViewset(viewsets.ModelViewSet):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    


# Class based view to Get User Details using Token Authentication
class UserDetailAPI(APIView):
  authentication_classes = (TokenAuthentication,)
  permission_classes = (AllowAny,)
  def get(self,request,*args,**kwargs):
    user = User.objects.get(id=request.user.id)
    serializer = UserSerializer(user)
    return Response(serializer.data)

#Class based view to register user
class RegisterUserAPIView(generics.CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = RegisterSerializer