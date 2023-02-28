from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from dashboard.models import Classroom, StudentClassroom
from attendance.models import AttendanceClass, Attendance, AttendanceTotal
import random
import datetime
import uuid

nUsers = 10
numdays = 30

class Command(BaseCommand):
    help = f'Creates {nUsers} users and assigns them to a class'

    def add_arguments(self, parser):
        parser.add_argument('Class_code', type=str, help='Class code to add users to')

    def handle(self, *args, **options):
        # add the user to the class
        classroom = Classroom.objects.get(join_code=options['Class_code'])
        if classroom is None:
            print("Classroom not found")
            return
        base = datetime.date.today()
        date_list = [base + datetime.timedelta(days=x) for x in range(0, numdays, 2)]
        students = StudentClassroom.objects.filter(classroom=classroom)

        for date in date_list:
            # check if attendanceClass object exists for this date
            if not AttendanceClass.objects.filter(date=date, course=classroom).exists():
                # create new attendanceClass object with new date
                attendance_class = AttendanceClass.objects.create(date=date, course=classroom)
                attendance_class.save()
                # create attendance object for each student
                for student in students:
                    attendance_obg = Attendance.objects.create(course=classroom, student=student.user,
                                                            att_class=attendance_class)
                    status = random.randint(0,1)
                    if(status==1):
                        attendance_obg.status = True
                    attendance_obg.save()


        for i in range(0,nUsers):
            userName = f'Student {random.randint(100,999)}'
            password = "test_password"
            # creaete a new user and add to Student group
            new_user = User.objects.create_user(username=userName, password=password)
            group, created = Group.objects.get_or_create(name='Student')
            group.user_set.add(new_user)
            # save the new user
            new_user.save()

            # Create a new student classroom object
            student_classroom = StudentClassroom.objects.create(user=new_user, classroom=classroom)
            student_classroom.save()

        print(f'Added {nUsers} users')