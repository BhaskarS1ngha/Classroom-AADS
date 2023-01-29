from django.shortcuts import redirect, render
from .models import Classroom, StudentClassroom, TeacherClassroom
# from helpers import random_str
from itertools import chain
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='auth/login')
def view_all_classrooms(request):
    print(request.user.username)
    if request.user.username == "":
        return HttpResponse("Hello")

    s = StudentClassroom.objects.filter(user=request.user)
    t = TeacherClassroom.objects.filter(user=request.user)
    classrooms = list(chain(s, t))

    return render(request, "dashboard/index.html", {
        "classrooms": classrooms
    })