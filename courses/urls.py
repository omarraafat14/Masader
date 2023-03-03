from django.urls import path , include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter(trailing_slash= False)
router.register('courses',views.CourseViewset)
router.register('groups/manager/users', views.ManagerViewSet)
router.register('groups/instructor/users', views.InstructorViewSet)
router.register('cart', views.CartViewSet, name='cart-detail'),
router.register('orders', views.OrderViewSet,basename = 'orders'),
router.register('order-items', views.OrderViewSet, basename='order-items')



urlpatterns = [
    path('', include(router.urls)),
    path('ratings', views.RatingsView.as_view()),
    path('payment', views.PaymentView.as_view()),
]
