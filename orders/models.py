from django.db import models
from django.contrib.auth.models import User
from courses.models import Course


# Create your models here.
class Order(models.Model):
    """represents an order made by a user, and has a total and a creation date"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, blank=True , null=True)


class OrderItem(models.Model):
    """Objects of the Order Model"""
    order = models.ForeignKey(Order, related_name='orders', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('order', 'course')