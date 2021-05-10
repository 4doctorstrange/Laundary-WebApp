from django.shortcuts import render, redirect, HttpResponse
from .forms import RegisterationForm, StudentForm, LoginForm, CycleForm, ContactAdminForm
from django.contrib import auth, messages
from .models import Student, UseCycle, ContactAdmin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .local import Utility
from datetime import datetime, timedelta, date
from .email import Email

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
            email = form_user.cleaned_data.get('email')
            user = User.objects.create_user(username=username, password = password, email=email)
            full_name =  form_student.cleaned_data.get("full_name")
            block = form_student.cleaned_data.get("block")
            room_no = form_student.cleaned_data.get("room_no")
            new_student = Student(full_name=full_name, block=block, user=user, room_no=room_no)
            new_student.save()
            '''sending EMail'''
            obj = Email()
            obj.register_email(email)   #telling user his account is been created
            
            ''' '''
            auth.login(request, user)
            #messages.success(request,"You have registered successfully! Please login to continue")
            return redirect('/')

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
                return redirect('/')
            else:
                login_form = LoginForm()
                messages.error(request,'Invalid credentials!')
                return render(request, 'login.html')
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
        data = UseCycle.objects.filter(student=request.user.student).all()
        today = date.today()
        to_be_updated = UseCycle.objects.filter(student=request.user.student, status=dic[1]).all()      #basically updating status if today>delivery date
        for i in to_be_updated: 
            if today >= i.delivery_date:
                i.status = dic[2]
                i.save()
                
        return render(request, 'dashboard.html', {'user':current_user, 'data': data})
    else:
        return redirect('/login')

def admin_dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        #DEbuggg
        
        if request.method == 'POST':
            reg = request.POST.get("reg")
            user = User.objects.filter(username=reg)   #here user is a query set
            if not user:
                messages.error(request,'Invalid registeration number entered')
                return redirect('/admin_dashboard')
            
            user = user[0]      #first and only element in query set is our target user
            student = Student.objects.filter(user=user)[0]
            data = UseCycle.objects.filter(student=student)
           
        else:
            data = UseCycle.objects.order_by('-date_time').all()
            
        return render(request, 'admin_dashboard.html', {'data':data})
        
        
    else:
        return redirect('/login')


def use_cycle(request):
    if request.method == "POST":
        num = request.POST.get("number")
        
        if num:     
            date_time = datetime.today()
            delivery_date = datetime.today() + timedelta(1)
            collection_info = None
            status = dic[1]
           
            cycle = UseCycle(student = request.user.student, no_of_clothes=num, date_time=date_time,
                   delivery_date=delivery_date, collection_info=collection_info, status=status )
            cycle.save()
            stu = Student.objects.filter(user = request.user)[0]
            stu.cycles_remaining-=1
            ''' sending Mail (once remaing cycles are less than 1, this mail will be send'''
            if stu.cycles_remaining<1:
                stu.cycles_remaining=0  
                obj = Email()
                to = request.user.email
                name = request.user.student.full_name
                obj.cycles_exhausted(to,name)
            ''' '''   

            stu.save()
            '''Sending checkin MAIL'''
            obj = Email()
            to = request.user.email
            print(request.user.email)
            data = [num, delivery_date]   #sending info like no of clothes and delivery date in the mail
            obj.checkin(to,data)
            '''        '''

            return redirect('/dashboard')
           
    else:
        #print(request.user.student.cycles_remaining)
        if request.user.is_authenticated:
            if request.user.student.cycles_remaining<1:
                return redirect('/dashboard')
            else:
                return render(request, 'use_cycle.html')

        else:
            return redirect('/login')

def collect(request, id):
    obj = UseCycle.objects.filter(pk=id)[0]
    delivery = obj.delivery_date
    today = date.today()
    collected = 0
    obj.status = dic[3]
    obj.collection_info = datetime.today()
    obj.save()
    '''sending Mail '''
    obj = Email()
    to = request.user.email
    obj.checkout(to)  #sends collection mail
    '''       '''
    messages.success(request, 'Laundary Collected!') 
    return redirect('/dashboard')

def contact_admin(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            contact_form = ContactAdminForm(request.POST)
            if contact_form.is_valid():
                cycles_needed = contact_form.cleaned_data.get('cycles_needed')
                username = request.user.username
                full_name = request.user.student.full_name
                entry = ContactAdmin(username=username, full_name=full_name, cycles_needed=cycles_needed)
                entry.save()
                return redirect('/dashboard')
        else:
            contact_form = ContactAdminForm()
            #print(contact_form)
            return render(request, 'contact_admin.html', {'contact_form':contact_form})

def view_requests(request):
    if request.user.is_authenticated and request.user.is_superuser:
        all_requests = ContactAdmin.objects.all()
    
        return render(request, 'view_requests.html', {'data': all_requests })
    else:
        return redirect('/login')

def confirm(request,id):
    if request.user.is_superuser:
        obj = ContactAdmin.objects.get(id=id)
        
        username= obj.username
        cycles_needed = obj.cycles_needed
        user = User.objects.filter(username=username)[0]
        student = Student.objects.filter(user=user)[0]
        student.cycles_remaining+=cycles_needed
        student.save()
    
        '''Sending confirmation via mail'''
        em=Email()
        em.confirmation(user.email)

        
        messages.success(request,'Request granted!')
        obj.delete()  #finally deleting object as it is no more a request
        return redirect('/admin_dashboard/view_requests')
    else:
        return redirect('/login')

def delete(request,id):
    if request.user.is_superuser:
        obj = ContactAdmin.objects.get(id=id)
        user = User.objects.filter(username=obj.username)[0]
        '''Sending confirmation via mail'''
        em=Email()
        em.delete(user.email)
        ''' ''' 
        obj.delete()
        messages.success(request,'Request removed!')
        return redirect('/admin_dashboard/view_requests')

    else:
        return redirect('/login')












