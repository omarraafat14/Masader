from django.urls import path , include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('courses',views.CourseViewset)
router.register('groups/manager/users', views.ManagerViewSet)
router.register('groups/instructor/users', views.InstructorViewSet)
router.register('cart/course-items', views.CartViewSet)
router.register('orders', views.OrderViewSet,basename = 'orders')
router.register('order-items', views.OrderViewSet, basename='order-items')



urlpatterns = [
    path('', include(router.urls)),
    path('ratings', views.RatingsView.as_view()),
]
