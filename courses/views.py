from datetime import date
from decouple import config
import requests

from .models import *
from .serializers import *
from .permissions import *
from .throttles import *

from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics , mixins , viewsets 


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

    # def destroy(self, request, *args, **kwargs):
    #     username = request.data.get('username')
    #     if username:
    #         user = get_object_or_404(User, username=username)
    #         manager_group = Group.objects.get(name='Manager')
    #         manager_group.user_set.remove(user)
    #         return Response(
    #             data = {'message': 'Manager has been deleted.'},
    #             status=status.HTTP_200_OK
    #         )
    #     return Response(
    #         data = {"message":"Error"},
    #         status=status.HTTP_400_BAD_REQUEST
    #     )


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


class PaymentView(APIView):
    def get(self, request):
        # Call first endpoint to get auth token
        api_key = config("API_KEY")
        headers = {"content-type": "application/json"}
        data = {
            "api_key": api_key,
        }
        response = requests.post("https://accept.paymob.com/api/auth/tokens", headers=headers, json=data)
        # print("response from step 1:", response.content)
        if response.status_code != 201:
            return Response({"error": "Failed to get auth token"}, status=response.status_code)
        token = response.json()["token"]

        # Call second endpoint to get order ID
        delivery_needed = "false"  # or True
        amount_cents = "100"  # replace with the actual amount in cents
        items = []  # replace with the actual items
        headers = {"content-type": "application/json", }
        data = {
            "auth_token": token,
            "delivery_needed": delivery_needed, 
            "amount_cents": amount_cents, 
            "items": items,
        }
        response = requests.post("https://accept.paymob.com/api/ecommerce/orders", headers=headers, json=data)
        # print("response from step 2:" , response.content)
        if response.status_code != 201:
            return Response({"error": "Failed to create order"}, status=response.status_code)
        order_id = response.json()["id"]

        # Call third endpoint to get payment key
        amount_cents = 100  # replace with the actual amount in cents
        expiration = 3600  # replace with the actual expiration time in seconds
        billing_data = {  # replace with the actual billing data
            "apartment": "NA", 
            "email": "claudette09@exa.com", 
            "floor": "NA", 
            "first_name": "Clifford", 
            "street": "NA", 
            "building": "NA", 
            "phone_number": "+86(8)9135210487", 
            "shipping_method": "NA", 
            "postal_code": "NA", 
            "city": "NA", 
            "country": "NA", 
            "last_name": "Nicolas", 
            "state": "NA",
        }
        currency = "EGP"  # replace with the actual currency code
        integration_id = 3384964  # replace with the actual integration ID
        headers = {"content-type": "application/json",}        
        data = {
        "auth_token": token,
        "amount_cents": str(amount_cents), 
        "expiration": expiration,
        "order_id": str(order_id),
        "billing_data": billing_data,
        "currency": currency, 
        "integration_id": integration_id,
        }
        response = requests.post("https://accept.paymob.com/api/acceptance/payment_keys", headers=headers, json=data)
        # print("Response from step 3:", response.content)
        if response.status_code != 201:
            return Response({"error": "Failed to get payment key"}, status=response.status_code)
        payment_key = response.json()["token"]

        # Return the payment key
        return redirect(f'https://accept.paymob.com/api/acceptance/iframes/730926?payment_token={payment_key}')
        # return Response({"payment_key": payment_key})


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return Cart.objects.all().filter(user = self.request.user)

    def create(self, request, *arg, **kwargs):
        serialized_item = CartSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)

        id = request.data['course']
        item = get_object_or_404(Course, id=id)
        course_price = item.price
        cart = Cart.objects.filter(user=request.user)
        course_prices = [course.course_price for course in cart]
        total_price = sum(course_prices)
        try:
            Cart.objects.create(
                user=request.user,  
                course_id=id, 
                course_price=course_price, 
                total_price=total_price
                )
        except:
            return Response(status=status.HTTP_409_CONFLICT, data={'message': 'Course already in cart'})
        return Response(status=status.HTTP_201_CREATED, data={'message':'Course added to cart!'})

    def destroy(self, request, *arg, **kwargs):
        if request.data['menuitem']:
            serialized_item = CartSerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            menuitem = request.data['menuitem']
            cart = get_object_or_404(Cart, user=request.user, menuitem=menuitem )
            cart.delete()
            return Response(status=status.HTTP_200_OK, data={'message':'Item removed from cart'})
        else:
            Cart.objects.filter(user=request.user).delete()
            return Response(status=status.HTTP_201_CREATED, data={'message':'All Items removed from cart'})





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
