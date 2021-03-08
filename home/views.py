from django.shortcuts import render, redirect, HttpResponse
from .forms import RegisterationForm, StudentForm, LoginForm, CycleForm
from django.contrib import auth, messages
from .models import Student, UseCycle
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .local import Utility
from datetime import datetime, timedelta, date

dic ={1: "unavailable", 2:"available", 3:"collected" }

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form_user = RegisterationForm(request.POST)
        form_student = StudentForm(request.POST)
        if form_user.is_valid() and form_student.is_valid():
            username = form_user.cleaned_data.get("username")
            password = form_user.cleaned_data.get("password2")
            user = User.objects.create_user(username=username, password = password)
            full_name =  form_student.cleaned_data.get("full_name")
            block = form_student.cleaned_data.get("block")
            room_no = form_student.cleaned_data.get("room_no")
            new_student = Student(full_name=full_name, block=block, user=user, room_no=room_no)
            new_student.save()
            auth.login(request, user)
            messages.add_message(request, messages.INFO, 'Successfully registered, please login to continue.')

    else:
        form_user = RegisterationForm()
        form_student = StudentForm()
    return render(request, 'register.html', { 'form_student': form_student, 'form_user': form_user})

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password) 
            if user:
                login(request, user)
                return redirect('/dashboard')
            else:
                login_form = LoginForm()
                return render(request, 'login.html', {'msg': 'Invalid credentials', 'login_form':login_form} )
        else:
            login_form = LoginForm()
            return render(request, 'login.html',{'login_form':login_form})
    else:
        return redirect('/')

def user_logout(request):
    logout(request)
    return redirect('/')

def user_dashboard(request):
    if request.user.is_authenticated:
        current_user = request.user
        fl = 0
        if current_user.is_superuser:
            data = UseCycle.objects.order_by('-date_time').all()
            fl = 1
        else:
            data = UseCycle.objects.filter(user=request.user.student).all()
            today = date.today()
            to_be_updated = UseCycle.objects.filter(user=request.user.student, status=dic[1]).all()      #basically updating status if today>delivery date
            for i in to_be_updated: 
                if today >= i.delivery_date:
                    i.status = dic[2]
                    i.save()
                

        return render(request, 'dashboard.html', {'user':current_user, 'data': data, 'fl':fl})
    else:
        return redirect('/login')

def use_cycle(request):
    if request.method == "POST":
        cf = CycleForm(request.POST)
        if cf.is_valid():
            num = cf.cleaned_data.get('no_of_clothes')
            
            date_time = datetime.today()
            delivery_date = datetime.today() + timedelta(1)
            collection_info = None
            status = dic[1]
            print('today', datetime.today())
            print('delivery', delivery_date)
            print(status)
            cycle = UseCycle(user = request.user.student, no_of_clothes=num, date_time=date_time,
                   delivery_date=delivery_date, collection_info=collection_info, status=status )
            cycle.save()

            stu = Student.objects.filter(user = request.user)[0]
            stu.cycles_remaining-=1
            stu.save()

            return redirect('/dashboard')
           
    else:
        cf = CycleForm()
        return render(request, 'use_cycle.html', {'cycle_form':cf})

def check(request):
    return render(request,'check.html')

def collect(request, id):
    obj = UseCycle.objects.filter(pk=id)[0]
    delivery = obj.delivery_date
    today = date.today()
    collected = 0
    if today >= delivery:
        obj.status = dic[3]
        obj.collection_info = datetime.today()
        obj.save()
    return redirect('/')