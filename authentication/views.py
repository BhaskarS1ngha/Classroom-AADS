from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import SignUpForm

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
                return redirect("home")
            else:
                messages.error(request, "Error creating user")
                return render(request=request, template_name="authentication/register.html", context={"form": form})
        else:
            for er in form.errors:
                errText = form.errors[er].as_text()
                messages.error(request, f"{errText[1:]}")
            return render(request=request, template_name="authentication/register.html", context={"form": form})

    form = SignUpForm
    return render(request=request, template_name="authentication/register.html", context={"form": form})


def login_view(request):
    pass


def logout_view(request):
    logout(request)
    return redirect('home')




