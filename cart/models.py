from django.db import models
from django.contrib.auth.models import User
from courses.models import Course

# Create your models here.
class Cart(models.Model):
    """represents a Cart which belongs to a user"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class CartItem(models.Model):
    """instances of a Cart model"""
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('course', 'cart')
