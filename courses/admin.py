from django.contrib import admin
from .models import *

# Register Course model.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'rating', 'price']
    search_fields = ['name']
    list_filter = ['name' , 'rating' , 'price']

# Register Instructor model.
@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'rating', 'students']
    search_fields = ['name']
    list_filter = ['name' , 'rating' , 'students']

# Register Chapter model.
admin.site.register(Chapter)

# Register video model.
admin.site.register(Video)