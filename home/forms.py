from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from .models import Student, UseCycle, ContactAdmin

class RegisterationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {'username':'Registeration Number'
                  }
    widgets = {'username': forms.TextInput(attrs={'class': 'form-control'}),
                   }

    error_messages = {'password_mismatch': 'Password do not match'}
                   
    
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['full_name', 'block', 'room_no']
        labels = {'full_name': 'Full Name', 'block': 'Block', 'room_no': 'Room Number'}

class LoginForm(forms.Form):
    username = forms.CharField(label='Registeration Number', max_length=100)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)

class CycleForm(forms.ModelForm):
    class Meta:
        model = UseCycle
        fields = ['no_of_clothes']
        labels = {'no_of_clothes': 'Number of clothes'}

class ContactAdminForm(forms.ModelForm):
    class Meta:
        model = ContactAdmin
        fields = ['cycles_needed']
        labels = {'cycles_needed' : 'Number of cycles required'}
