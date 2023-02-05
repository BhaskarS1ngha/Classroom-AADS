import json
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from dashboard.models import Classroom, StudentClassroom, TeacherClassroom
from itertools import chain
# Create your views here.


@login_required(login_url='/auth/login')
def get_classrooms(request):
    s = StudentClassroom.objects.filter(user=request.user)
    t = TeacherClassroom.objects.filter(user=request.user)
    classes = list(chain(s,t))
    data = list()
    for x in classes:
        d = {
            'title': x.classroom.title,
            'desc': x.classroom.description,
            'code': x.classroom.join_code,
        }
        data.append(d)
    dump = json.dumps(data)
    return JsonResponse(data,safe=False)