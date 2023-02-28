from django.shortcuts import render, get_object_or_404, redirect
from .models import Attendance, AttendanceClass
from dashboard.models import StudentClassroom, Classroom
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime

# Create your views here.

@login_required(login_url='/auth/login')
def confirm(request, attendance_id):
    if request.method == 'POST':
        print(request.POST)
        attendance_class = get_object_or_404(AttendanceClass, id=attendance_id)
        class_room = get_object_or_404(Classroom, join_code=attendance_class.course.join_code)
        students = StudentClassroom.objects.filter(classroom=class_room)
        # get date from post
        date = request.POST.get('date')


        # check if attendanceClass object exists for this date
        if not AttendanceClass.objects.filter(date=date, course=class_room).exists():

            # create new attendanceClass object with new date
            attendance_class = AttendanceClass.objects.create(date=date, course=class_room)
            attendance_class.save()


            # create attendance object for each student
            for student in students:
                attendance_obg = Attendance.objects.create(course=class_room, student=student.user,
                                                           att_class=attendance_class)
                attendance_obg.save()
        attendance_list = Attendance.objects.filter(course=class_room, att_class=attendance_class)
        for student in students:
            attendance_obg = Attendance.objects.get(course=class_room, student=student.user,
                                                    att_class=attendance_class)
            try:
                status = request.POST[f'{student.user.id}']
                attendance_obg.status = True
                print(status)
            except KeyError:
                print("Value not found, student_id = ",student.user.id)

            # update atttendance status for each student
            # attendance_obg = Attendance.objects.get(course=class_room, student=student.user,
            #                                         att_class=attendance_class)

            attendance_obg.save()
        messages.success(request, "Attendance has been taken successfully")
        return redirect('dashboard:classroom', code=class_room.join_code)
    else:
        messages.error(request, "Error taking attendance")
        return redirect('dashboard:home')


@login_required(login_url='/auth/login')
def create_attendance(request, class_code):
    """
    view that creates an attendance object for each user in Student group
    :param request:
    :param class_code:
    """

    date = datetime.date.today()
    # check if user is a teacher
    if request.user.groups.filter(name='Faculty').exists():
        # get classroom object or raise 404 error
        class_room = get_object_or_404(Classroom, join_code=class_code)
        # get all students in class
        students = StudentClassroom.objects.filter(classroom=class_room)

        # check if attendance has already been taken for today
        if AttendanceClass.objects.filter(date=date, course=class_room).exists():
            attendance_class = AttendanceClass.objects.get(date=date, course=class_room)

            # check if any new student has been added since last attendance
            for student in students:
                if not Attendance.objects.filter(course=class_room, student=student.user,
                                                 att_class=attendance_class).exists():
                    attendance_obg = Attendance.objects.create(course=class_room, student=student.user,
                                                               att_class=attendance_class)
                    attendance_obg.save()

            attendance_list = Attendance.objects.filter(course=class_room, att_class=attendance_class)
            return render(request, 'attendance/attendance.html',
                          {'attendance': attendance_list, 'attendance_class': attendance_class})

        # create new Attendance class object with today's date
        attendance_class = AttendanceClass.objects.create(date=date, course=class_room)
        attendance_class.save()

        # create attendance object for each student
        for student in students:
            attendance_obg = Attendance.objects.create(course=class_room, student=student.user,
                                                       att_class=attendance_class)
            attendance_obg.save()
        attendance_list = Attendance.objects.filter(course=class_room, att_class=attendance_class)
        return render(request, 'attendance/attendance.html',
                      {'attendance': attendance_list, 'attendance_class': attendance_class})
    else:
        return render(request, 'dashboard/index.html')




# def attendance(request):
#     """
#     view that returns an html render with Attendance as context
#     :param request:
#     """
#     attendance = Attendance()
#     return render(request, 'attendance/attendance.html', {'attendance': attendance})