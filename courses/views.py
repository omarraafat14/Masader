from datetime import date
from django.shortcuts import render, get_object_or_404
from rest_framework import generics , mixins , viewsets 
from .models import *
from .serializers import *
from .permissions import *
from .throttles import *
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle



# Create Viewsets endpoint
class CourseViewset(viewsets.ModelViewSet):
    queryset = Course.objects.all()    
    serializer_class = CourseSerializer
    throttle_classes = [UserRateThrottle,AnonRateThrottle]
    ordering_fields=['rating']
    search_fields = ['title']

    
    def get_permissions(self):
        permission_classes = []
        if(self.request.method !='GET'):
            permission_classes = [IsManager | IsInstructor]
        return[permission() for permission in permission_classes]


class ChapterViewset(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    throttle_classes = [UserRateThrottle,AnonRateThrottle]
    
class VideoViewset(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    throttle_classes = [UserRateThrottle,AnonRateThrottle]

class FAQViewset(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

class RatingsView(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    throttle_classes = [UserRateThrottle,AnonRateThrottle]

    def get_permissions(self):
        if(self.request.method=='GET'):
            return []    
        return [IsAuthenticated()]

    def get_queryset(self):
        return Rating.objects.all().filter(user = self.request.user)

class ManagerViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(groups__name='Manager')
    serializer_class = UserSerializer
    permission_classes=[IsManager]
    throttle_classes = [UserRateThrottle,AnonRateThrottle]
    # need to be re-viewed
    def create(self, request):
        username = request.data.get('username')
        if username:
            user = get_object_or_404(User, username=username)
            manager_group = Group.objects.get(name='Manager')
            manager_group.user_set.add(user)
            return Response(
                status=status.HTTP_201_CREATED, 
                data={'message': 'User added to Manager group.'}
                )

        return Response(
            data = {"message":"Error"},
            status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, *args, **kwargs):
        username = request.data.get('username')
        if username:
            user = get_object_or_404(User, username=username)
            manager_group = Group.objects.get(name='Manager')
            manager_group.user_set.remove(user)
            return Response(
                data = {'message': 'Manager has been deleted.'},
                status=status.HTTP_200_OK
            )
        return Response(
            data = {"message":"Error"},
            status=status.HTTP_400_BAD_REQUEST
        )


class InstructorViewSet(viewsets.ModelViewSet):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    throttle_classes = [UserRateThrottle,AnonRateThrottle]

    def get_permissions(self):
        permission_classes = [IsInstructor]
        if(self.request.method =='DELETE'):
            permission_classes = [IsManager]
        return[permission() for permission in permission_classes]

    def destroy(self, request, *args, **kwargs):
        username = request.data.get('username')
        if username:
            user = get_object_or_404(User, username=username)
            manager_group = Group.objects.get(name='Delivery crew')
            manager_group.user_set.remove(user)
            return Response(
                data = {'message': 'Delivery has been deleted.'},
                status=status.HTTP_200_OK
            )
        return Response(
            data = {"message":"Error"},
            status=status.HTTP_400_BAD_REQUEST
        )


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsStudent]
    throttle_classes = [UserRateThrottle,AnonRateThrottle]

    def get_queryset(self):
        return Cart.objects.all().filter(user = self.request.user)

    def create(self, request, *arg, **kwargs):
        serialized_item = CartSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)

        id = request.data['course']
        cart = Cart.objects.filter(user=request.user)
        course_prices = [course.price for course in cart.courses.all()]
        total_price = sum(course_prices)

        item = get_object_or_404(Course, id=id)
        course_price = item.price
        try:
            Cart.objects.create(user=request.user,  course_id=id, course_price=course_price, total_price=total_price,)
        except:
            return Response(status=status.HTTP_409_CONFLICT, data={'message': 'Item already in cart'})
        return Response(status=status.HTTP_201_CREATED, data={'message':'Item added to cart!'})

    def destroy(self, request, *arg, **kwargs):
        if request.data['course']:
            serialized_item = CartSerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            course = request.data['course']
            cart = get_object_or_404(Cart, user=request.user, course=course)
            cart.delete()
            return Response(status=status.HTTP_200_OK, data={'message':'Course removed from cart'})
        else:
            Cart.objects.filter(user=request.user).delete()
            return Response(status=status.HTTP_201_CREATED, data={'message':'All Courses removed from cart'})


class OrderViewSet(viewsets.ViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderSerializer
    throttle_classes = [UserRateThrottle,AnonRateThrottle]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Student').exists():
            return Order.objects.all().filter(user = user)
        elif user.groups.filter(name='Instructor').exists():
            return Order.objects.all().filter(user = user)
        else:
            return Order.objects.all()

    def get_permissions(self):
        permission_classes = []
        if self.request.method in ['GET', 'POST']:
            permission_classes = [IsStudent | IsManager | IsInstructor]
        elif self.request.method == 'DELETE':
            permission_classes = [IsManager]
        elif self.request.method == 'PATCH':
            permission_classes = [IsInstructor]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        cart = Cart.objects.filter(user = request.user)
        lis = cart.values_list()
        if len(lis) == 0:
            return Response(data={"Error":"Cart is empty"},status=status.HTTP_400_BAD_REQUEST)
        
        total = sum([course.price for course in cart])
        order = Order.objects.create(
            user=request.user, 
            total=total,
            status=False, 
            date=date.today()
        )
        for item in cart.values():
            course = get_object_or_404(Course, id=item['course'])
            orderitem = OrderItem.objects.create(
                order=order, 
                course=course, 
            )
            orderitem.save()
        cart.delete()
        return Response(status=201, data={'message':'Your order has been placed! Your order number is {}'.format(str(order.id))})


class SingleOrderView(generics.ListCreateAPIView):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()
    throttle_classes = [UserRateThrottle,AnonRateThrottle]
    
    def get_permissions(self):
        order = Order.objects.get(pk=self.kwargs['pk'])
        if self.request.user == order.user and self.request.method == 'GET':
            permission_classes = [IsStudent]
        elif self.request.method == 'PUT' or self.request.method == 'DELETE':
            permission_classes = [IsStudent, IsManager]
        else:
            permission_classes = [IsStudent, IsInstructor | IsManager]
        return[permission() for permission in permission_classes]

    def get_queryset(self, *args, **kwargs):
            return OrderItem.objects.filter(order_id=self.kwargs['pk'])

    def patch(self, request, *args, **kwargs):
        order = Order.objects.get(pk=self.kwargs['pk'])
        order.status = not order.status
        order.save()
        return Response(status=200, data={'message':'Status of order #'+ str(order.id)+' changed to '+str(order.status)})


    def delete(self, request, *args, **kwargs):
        order = Order.objects.get(pk=self.kwargs['pk'])
        order_number = str(order.id)
        order.delete()
        return Response(status=200, data={'message':'Order #{} was deleted'.format(order_number)})
