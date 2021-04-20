from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('user_register', views.register, name="user_register"),
    path('login', views.user_login, name="login"),
    path('logout', views.user_logout, name="logout"),
    path('dashboard', views.user_dashboard, name="user_dashboard"),
    path('use_cycle', views.use_cycle, name="use_cycle"),
    #path('check', views.check, name="check"),
    path('collect/<int:id>', views.collect, name="collect"),
    
    

    

    
    

]
