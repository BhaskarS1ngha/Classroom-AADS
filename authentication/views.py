import json

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import JsonResponse
from .forms import SignUpForm, LoginForm
from django.contrib.auth.models import Group
from dashboard.models import Classroom, StudentClassroom, TeacherClassroom

# Create your views here.


def home(request):
    return render(request=request, template_name="index.html")


def register(request):
    if request.method=="POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                username = form.cleaned_data.get('username')
                login(request=request,user=user)
                messages.success(request, f"User: {username} Created")
                messages.info(request,f"You are now logged in as {username}")
                return redirect("dashboard:home")
            else:
                messages.error(request, "Error creating user")
                return render(request=request, template_name="authentication/register.html", context={"form": form})
        else:
            print("error")
            for er in form.errors:
                errText = form.errors[er].as_text()
                messages.error(request, f"{errText[1:]}")
                print(errText)
            return render(request=request, template_name="authentication/register.html", context={"form": form})

    form = SignUpForm
    return render(request=request, template_name="authentication/register.html", context={"form": form})


def login_view(request):
    if request.method == "POST":
        form=LoginForm(request=request,data=request.POST)

        if form.is_valid():
            user_name=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=user_name,password=password)
            if user is not None:
                login(request,user)
                messages.success(request, "Logged in!")
                return redirect('dashboard:home')
        else:
            messages.error(request,"Please try again")
            return render(request,'authentication/login.html',{'form':form})
    form=LoginForm()
    return render(request,'authentication/login.html',{'form':form})


def logout_view(request):
    logout(request)
    return redirect('dashboard:home')


def get_classrooms(request):
    data = {
        'Name' : 'AOS',
        'Instructor':  'Prof 1',
        'Student_count': '80'
    }
    dump = json.dumps(data)
    return HttpResponse(dump,content_type='application/json')




