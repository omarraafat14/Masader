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



class CartView(generics.RetrieveUpdateAPIView):
    """represent a single model instance."""
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Returns an object instance that should be used for detail views."""
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart
    


class AddToCartView(generics.CreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsStudent]

    def post(self, request, *arg, **kwargs):
        course_id = request.data.get('course_id')
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


class CreateOrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsStudent]
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
