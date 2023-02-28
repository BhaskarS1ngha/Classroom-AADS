from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from dashboard.models import Classroom, StudentClassroom
import random
import uuid

nUsers = 10

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

        for i in range(0,nUsers):
            k=0
            userName = f'CSE220{random.randint(10,99)}'
            password = "test_password"

            while(User.objects.filter(username=userName).exists()):
                print(f'User {userName} already exists, regenerating')
                userName = f'CSE220{random.randint(10,99)}'
                k+=1
                if k>90:
                    print("Too many users with same name, aborting")
                    return


            # create a new user and add to Student group
            new_user = User.objects.create_user(username=userName, password=password)
            group, created = Group.objects.get_or_create(name='Student')
            group.user_set.add(new_user)
            # save the new user
            new_user.save()

            # Create a new student classroom object
            student_classroom = StudentClassroom.objects.create(user=new_user, classroom=classroom)
            student_classroom.save()

        print(f'Added {nUsers} users')