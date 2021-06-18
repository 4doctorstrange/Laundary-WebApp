from django.contrib import admin
from .models import Student, UseCycle, ContactAdmin
# Register your models here.
#admin.site.register(Student)
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user','full_name','cycles_remaining']

@admin.register(ContactAdmin)
class Contact_Admin(admin.ModelAdmin):
    list_display = ['id','username','full_name','cycles_needed']

@admin.register(UseCycle)
class UseCycleAdmin(admin.ModelAdmin):
    list_display = ['id','student','no_of_clothes']

