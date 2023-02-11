from django.contrib import admin
from .models import *

# Register Course model.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'price']
    search_fields = ['title']
    list_filter = ['title' , 'price']

# Register Instructor model.
@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'students']
    search_fields = ['name']
    list_filter = ['name', 'students']

# Register Chapter model.
admin.site.register(Chapter)

# Register video model.
admin.site.register(Video)

# Register FAQ model.
admin.site.register(FAQ)

admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)