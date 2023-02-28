from django.shortcuts import redirect, render, get_object_or_404
from .models import Classroom, StudentClassroom, TeacherClassroom
# from helpers import random_str
from itertools import chain
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from string import ascii_lowercase
import random


# Create your views here.
@login_required(login_url='/auth/login')
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


def random_str(digit=7):
    return "".join([random.choice(ascii_lowercase) for _ in range(digit)])


@login_required(login_url='/auth/login')
def create_classroom(request):
    # check if user is a faculty
    if not request.user.groups.filter(name="Faculty").exists():
        return HttpResponse("You are not a faculty")
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        join_code = random_str()

        """
        Add try-except here to catch duplicate classes
        """
        c = Classroom.objects.create(title=title, description=description, owner=request.user, join_code=join_code)
        TeacherClassroom.objects.create(user=request.user, classroom=c)

        return redirect("/")

    else:
        return render(request, "dashboard/create.html")


@login_required(login_url='/auth/login')
def join_classroom(request):
    if request.method == "POST":
        code = request.POST["code"]

        """
                Add try-except here to catch invalid join code
        """
        classroom = Classroom.objects.get(join_code=code)
        StudentClassroom.objects.create(user=request.user, classroom=classroom)

        return redirect(f"/classroom/{code}/")

    else:
        return render(request, "dashboard/join-classroom.html")


@login_required(login_url='/auth/login')
def view_classroom(request, code):
    classroom = get_object_or_404(Classroom, join_code=code)
    students = StudentClassroom.objects.filter(classroom=classroom)
    return render(request, "dashboard/class.html", {
        "classroom": classroom,
        "students": students,
    })