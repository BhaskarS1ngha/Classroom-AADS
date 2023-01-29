import json
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='/auth/login')
def get_classrooms(request):
    data = {
        'Name' : 'AOS',
        'Instructor':  'Prof 1',
        'Student_count': '80'
    }
    # dump = json.dumps(data)
    return JsonResponse(data)