from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Count
from django.core.validators import MinValueValidator , MaxValueValidator
# Create your models here.


class Course(models.Model):
    """Create database model of Courses"""
    name = models.CharField(max_length=200,default='Lorem ipsum')
    summary = models.CharField(max_length= 400,default='Lorem ipsum')
    category = models.CharField(max_length= 200,default='Lorem ipsum')
    rating = models.DecimalField(
        max_digits=2 ,decimal_places=1,default=4.5,
        validators=[MinValueValidator(1.0) , MaxValueValidator(5.0)]
        )
    last_update = models.DateField(default=2022-11-27)
    language = models.CharField(max_length= 200,default='Lorem ipsum')
    subtitle = models.CharField(max_length= 200,default='Lorem ipsum')
    price = models.IntegerField(default=199)
    description = models.CharField(max_length= 600,default='Lorem ipsum')
    overview = models.CharField(max_length= 600,default='Lorem ipsum')
    instructors = models.ManyToManyField("Instructor" , related_name= 'courses', null=True)

    def __str__(self):
        return self.name


class Chapter(models.Model):
    course = models.ForeignKey(Course, related_name='chapters', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

class Video(models.Model):
    title = models.CharField(max_length=250)
    # video = models.FileField(upload_to=user_directory_path)
    chapter = models.ForeignKey(Chapter, related_name='videos', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

class Instructor(models.Model):
    """Create database model of Instructor"""
    name = models.CharField(max_length= 40)
    image = models.ImageField(upload_to="images\\instructors" , default="avatar.png")
    rating = models.DecimalField(
        max_digits=2 , decimal_places=1,default=4.0,
        validators=[MinValueValidator(1.0) , MaxValueValidator(5.0)]
        )
    reviews  = models.IntegerField(default=100)
    students = models.IntegerField(default=1000)
    summary = models.CharField(max_length= 400,default='Lorem ipsum')

    def no_of_courses(self):
        count = Course.objects.filter(instructors = self)
        return len(count)

    # def my_courses(self):
    #     count = Course.objects.get("name").filter(instructors = self)
    #     return count

    def __str__(self):
        return self.name
    
    


@receiver(post_save , sender = settings.AUTH_USER_MODEL)
def token_user(sender , instance , created , **kwargs):
    if created:
        Token.objects.create(user = instance)