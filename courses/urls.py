from django.urls import path , include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from . import views

router = DefaultRouter()
router.register("courses" , views.viewsete_courses)
router.register("instructors", views.InstructorViewset)

urlpatterns = [
    # path('courses' , views.mixins_list.as_view() , name = 'list'),
    # path('courses/<int:pk>' , views.mixins_pk.as_view() , name = 'pk')
    path('api/' , include(router.urls)),
    path('token' , obtain_auth_token),
    path("get-details",views.UserDetailAPI.as_view()),
    path('register',views.RegisterUserAPIView.as_view()),
]
