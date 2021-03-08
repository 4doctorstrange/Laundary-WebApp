from django.contrib import admin
from .models import Student, UseCycle
# Register your models here.
@admin.register(Student)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'full_name']

@admin.register(UseCycle)
class Cycles(admin.ModelAdmin):
    list_display = ['id', 'user', 'date_time']
