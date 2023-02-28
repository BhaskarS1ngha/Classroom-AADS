from django.shortcuts import render, get_object_or_404, redirect
from .models import Attendance, AttendanceClass, AttendanceTotal
from dashboard.models import StudentClassroom, Classroom
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime

# Create your views here.

# @login_required(login_url='/auth/login')
# def confirm(request, attendance_id):
#     if request.method == 'POST':
#         print(request.POST)
#         attendance_class = get_object_or_404(AttendanceClass, id=attendance_id)
#         class_room = get_object_or_404(Classroom, join_code=attendance_class.course.join_code)
#         students = StudentClassroom.objects.filter(classroom=class_room)
#         # get date from post
#         date = request.POST.get('date')
#
#
#         # check if attendanceClass object exists for this date
#         if not AttendanceClass.objects.filter(date=date, course=class_room).exists():
#
#             # create new attendanceClass object with new date
#             attendance_class = AttendanceClass.objects.create(date=date, course=class_room)
#             attendance_class.save()
#
#
#             # create attendance object for each student
#             for student in students:
#                 attendance_obg = Attendance.objects.create(course=class_room, student=student.user,
#                                                            att_class=attendance_class)
#                 attendance_obg.save()
#         attendance_list = Attendance.objects.filter(course=class_room, att_class=attendance_class)
#         for student in students:
#             attendance_obg = Attendance.objects.get(course=class_room, student=student.user,
#                                                     att_class=attendance_class)
#             try:
#                 status = request.POST[f'{student.user.id}']
#                 attendance_obg.status = True
#                 print(status)
#             except KeyError:
#                 print("Value not found, student_id = ",student.user.id)
#
#             # update atttendance status for each student
#             # attendance_obg = Attendance.objects.get(course=class_room, student=student.user,
#             #                                         att_class=attendance_class)
#
#             attendance_obg.save()
#         messages.success(request, "Attendance has been taken successfully")
#         return redirect('dashboard:classroom', code=class_room.join_code)
#     else:
#         messages.error(request, "Error taking attendance")
#         return redirect('dashboard:home')



@login_required(login_url='/auth/login')
def confirm(request, class_code):
    if request.method == 'POST':
        print(request.POST)
        class_room = get_object_or_404(Classroom, join_code=class_code)
        students = StudentClassroom.objects.filter(classroom=class_room)
        # get date from post
        date = request.POST.get('date')

        # check if attendanceClass object exists for this date
        if AttendanceClass.objects.filter(date=date, course=class_room).exists():
            messages.error(request, "Attendance has already been taken for this date")
            return redirect('dashboard:classroom', code=class_room.join_code)

        # create new attendanceClass object with date
        attendance_class = AttendanceClass.objects.create(date=date, course=class_room)
        attendance_class.save()

        # create attendance object for each student
        for student in students:
            attendance_obg = Attendance.objects.create(course=class_room, student=student.user,
                                                       att_class=attendance_class)
            try:
                status = request.POST[f'{student.user.id}']
                attendance_obg.status = True
                print(status)
            except KeyError:
                print("Value not found, student_id = ",student.user.id)
            attendance_obg.save()

        messages.success(request, "Attendance has been taken successfully")
        return redirect('dashboard:classroom', code=class_room.join_code)
    else:
        messages.error(request, "Error taking attendance")
        return redirect('dashboard:home')


# @login_required(login_url='/auth/login')
# def create_attendance(request, class_code):
#     """
#     view that creates an attendance object for each user in Student group
#     :param request:
#     :param class_code:
#     """
#
#     date = datetime.date.today()
#     # check if user is a teacher
#     if request.user.groups.filter(name='Faculty').exists():
#         # get classroom object or raise 404 error
#         class_room = get_object_or_404(Classroom, join_code=class_code)
#         # get all students in class
#         students = StudentClassroom.objects.filter(classroom=class_room)
#         students = sorted(students, key=lambda x: x.user.username)
#
#         # check if attendance has already been taken for today
#         if AttendanceClass.objects.filter(date=date, course=class_room).exists():
#             attendance_class = AttendanceClass.objects.get(date=date, course=class_room)
#
#             # check if any new student has been added since last attendance
#             for student in students:
#                 if not Attendance.objects.filter(course=class_room, student=student.user,
#                                                  att_class=attendance_class).exists():
#                     attendance_obg = Attendance.objects.create(course=class_room, student=student.user,
#                                                                att_class=attendance_class)
#                     attendance_obg.save()
#
#             attendance_list = Attendance.objects.filter(course=class_room, att_class=attendance_class).order_by('student__username')
#             # attendance_list1 = sorted(attendance_list, key=lambda x: x.student.username)
#             print(type(attendance_list))
#             return render(request, 'attendance/attendance.html',
#                           {'attendance': attendance_list, 'attendance_class': attendance_class})
#
#         # create new Attendance class object with today's date
#         attendance_class = AttendanceClass.objects.create(date=date, course=class_room)
#         attendance_class.save()
#
#         # create attendance object for each student
#         for student in students:
#             attendance_obg = Attendance.objects.create(course=class_room, student=student.user,
#                                                        att_class=attendance_class)
#             attendance_obg.save()
#         attendance_list = Attendance.objects.filter(course=class_room, att_class=attendance_class)
#         attendance_list = sorted(attendance_list, key=lambda x: x.student.username)
#         for _ in attendance_list:
#             print(_.student.username)
#         return render(request, 'attendance/attendance.html',
#                       {'attendance': attendance_list, 'attendance_class': attendance_class})
#     else:
#         return render(request, 'dashboard/index.html')


@login_required(login_url='/auth/login')
def new_attendance(request,class_code):
    if request.user.groups.filter(name='Faculty').exists():
        # get classroom object or raise 404 error
        class_room = get_object_or_404(Classroom, join_code=class_code)
        # get all students in class
        students = StudentClassroom.objects.filter(classroom=class_room).order_by('user__username')
        return render(request, 'attendance/attendance.html', {'students': students})
    else:
        return render(request, 'dashboard/index.html')


@login_required(login_url='/auth/login')
def view_attendance(request,class_code,student_id):
    '''
    view that returns an html render with the detailed attendance of a student
    :param request:
    :param class_code:
    :param student_id:
    :return:
    '''
    # get classroom object or raise 404 error
    class_room = get_object_or_404(Classroom, join_code=class_code)
    # get student object or raise 404 error
    student = get_object_or_404(User, id=student_id)
    # get all attendance objects for this student
    attendance_list = Attendance.objects.filter(course=class_room, student=student).order_by('att_class__date')

    # get attendanceTotal object for this student
    if AttendanceTotal.objects.filter(student=student, course=class_room).exists():
        attendance_total = AttendanceTotal.objects.get(student=student, course=class_room)
    else:
        attendance_total = AttendanceTotal.objects.create(student=student, course=class_room)

    context = {
        'attendance': attendance_list,
        'student': student,
        'classroom': class_room,
        'attendance_total': attendance_total
    }
    return render(request, 'attendance/view_attendance.html', context)



