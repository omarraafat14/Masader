from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Group

class IsManager(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='Manager').exists():
            return True
        return False

class IsInstructor(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='Instructor').exists():
            return True
        return False

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        groups = Group.objects.filter(name__in=['Manager', 'Instructor'])
        user_groups = request.user.groups.filter(pk__in=groups)
        if user_groups.exists():
            return False
        else:
            return True
