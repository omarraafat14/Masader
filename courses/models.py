from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator , MaxValueValidator
import datetime


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255)

    def __str__(self) -> str:
        return self.title
     

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.DecimalField(
        max_digits=2 ,decimal_places=1,default=2.5,
        validators=[MinValueValidator(1.0) , MaxValueValidator(5.0)]
        )
    course = models.ForeignKey('Course', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'course')


class Course(models.Model):
    """Create database model of Courses"""
    category = models.ForeignKey(Category, on_delete=models.PROTECT,default=1)
    title = models.CharField(max_length=255,db_index=True,default='Lorem ipsum')
    summary = models.CharField(max_length= 400,default='Lorem ipsum')
    last_update = models.DateField(default=2022-11-27)
    language = models.CharField(max_length= 200,default='English')
    subtitle = models.CharField(max_length= 200,default='English')
    price = models.DecimalField(max_digits=6,decimal_places=2,db_index=True)
    # description = models.CharField(max_length= 600,default='Lorem ipsum')
    # overview = models.CharField(max_length= 600,default='Lorem ipsum')
    
    # Relationships between Course and (Instructor + Chapter)
    # chapter = models.ForeignKey("Chapter",on_delete=models.PROTECT, related_name='chapters',default="chapter")
    
    def __str__(self):
        return self.title


class Instructor(models.Model):
    """Create database model of Instructor"""
    name = models.CharField(max_length= 50 , db_index=True)
    image = models.ImageField(upload_to="images\\instructors" , default="avatar.png")
    reviews  = models.IntegerField(default=100)
    students = models.IntegerField(default=1000)
    summary = models.CharField(max_length= 400,default='Lorem ipsum')
    course = models.ManyToManyField(Course, blank=True)
    # Function to get count of Courses which taught by same Instructor
    def no_of_courses(self):
        count = Course.objects.filter(instructors = self)
        return len(count)

    def __str__(self):
        return self.name


class Chapter(models.Model):
    """Create database model of Chapter"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # Relationship between Chapter and its Videos
    course = models.ForeignKey(Course, related_name='chapters',on_delete=models.CASCADE,default=None)
    def __str__(self):
        return self.title


class Video(models.Model):
    """Create database model of Video"""
    title = models.CharField(max_length=25, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    summary = models.CharField(max_length= 255,default="summary")
    chapter = models.ForeignKey(Chapter, on_delete=models.PROTECT)
    def __str__(self):
        return self.title


class FAQ(models.Model):
    HEADER = 2
    ACTIVE = 1
    INACTIVE = 0
    STATUS_CHOICES = (
        (ACTIVE,  ('Active')),
        (INACTIVE, ('Inactive')),
        (HEADER,  ('Group Header')),
    )
    
    text = models.TextField(('question'), help_text=   ('The actual question itself.'))
    answer = models.TextField(('answer'), blank=True, help_text= ('The answer text.'))
    chapter = models.ForeignKey(Chapter, verbose_name= ('chapter'), related_name='questions',on_delete=models.PROTECT)
    slug = models.SlugField(('slug'), max_length=100)
    status = models.IntegerField(('status'),
        choices=STATUS_CHOICES, default=INACTIVE, 
        help_text= ("Only questions with their status set to 'Active' will be "
                    "displayed. Questions marked as 'Group Header' are treated "
                    "as such by views and templates that are set up to use them."))
    
    protected = models.BooleanField(('is protected'), default=False,
        help_text= ("Set true if this question is only visible by authenticated users."))
        
    sort_order = models.IntegerField( ('sort order'), default=0,
        help_text= ('The order you would like the question to be displayed.'))

    created_on = models.DateTimeField( ('created on'), default=datetime.datetime.now)
    updated_on = models.DateTimeField( ('updated on'))
    created_by = models.ForeignKey(User, verbose_name= ('created by'),
        null=True, related_name="+",on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, verbose_name= ('updated by'),
        null=True, related_name="+",on_delete=models.CASCADE)  
        
    class Meta:
        verbose_name =  ("Frequent asked question")
        verbose_name_plural =  ("Frequently asked questions")
        ordering = ['sort_order', 'created_on']

    def __str__(self):
        return self.text

    

# # Create Auto token when new user signed in
# @receiver(post_save , sender = settings.AUTH_USER_MODEL)
# def token_user(sender , instance , created , **kwargs):
#     if created:
#         Token.objects.create(user = instance)