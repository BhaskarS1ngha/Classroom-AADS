from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm

# Create your views here.


def register(request):
    if request.method=="POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = SignUpForm
        return render(request=request,
                      template_name="authentication/register.html",
                      context={"form": form})


def login_view(request):
    pass


def logout_view(request):
    pass


def home(request):
    return render(request=request, template_name="index.html")

