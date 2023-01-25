from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm

# Create your views here.


def home(request):
    return render(request=request, template_name="index.html")


def register(request):
    if request.method=="POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request=request,user=user)
            return redirect("home")
    else:
        form = SignUpForm
        return render(request=request,
                      template_name="authentication/register.html",
                      context={"form": form})


# def login_view(request):
#     pass


class UserAuthenticationForm:
    pass


def login_view(request):
    if request.method=="POST":
        form=UserAuthenticationForm(request=request,data=request.POST)
        if form.is_valid():
            user_name=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=user_name,password=password)
            if user!=None:
                login(request,user)
                return redirect('home')
        else:
            return render(request,'authentication/login.html',{'form':form})
    form=UserAuthenticationForm()
    return render(request,'authentication/login.html',{'form':form})


def logout_view(request):
    logout(request)
    return redirect('home')




