from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from dashboard.models import Classroom
from django.contrib.auth.models import User
import math
import datetime

# Create your models here.

class AttendanceClass(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)



class Attendance(models.Model):
    course = models.ForeignKey(Classroom,on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    att_class = models.ForeignKey(AttendanceClass, on_delete=models.CASCADE)
    status = models.BooleanField(default='False')

    def __str__(self):
        sname = User.objects.get(name=self.student.name)
        cname = Classroom.objects.get(title=self.course)
        return '%s : %s' % (sname.name, cname.title)



class AttendanceTotal(models.Model):
    course = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('student', 'course'),)

    @property
    def att_class(self):
        stud = User.objects.get(name=self.student.name)
        cr = Classroom.objects.get(title=self.course.title)
        att_class = Attendance.objects.filter(course=cr, student=stud, status='True').count()
        return att_class

    @property
    def total_class(self):
        stud = User.objects.get(name=self.student.name)
        cr = Classroom.objects.get(title=self.course.title)
        total_class = Attendance.objects.filter(course=cr, student=stud).count()
        return total_class

    @property
    def attendance(self):
        stud = User.objects.get(name=self.student.name)
        cr = Classroom.objects.get(title=self.course.title)
        total_class = Attendance.objects.filter(course=cr, student=stud).count()
        att_class = Attendance.objects.filter(course=cr, student=stud, status='True').count()
        if total_class == 0:
            attendance = 0
        else:
            attendance = round(att_class / total_class * 100, 2)
        return attendance

    @property
    def classes_to_attend(self):
        stud = User.objects.get(name=self.student.name)
        cr = Classroom.objects.get(title=self.course.title)
        total_class = Attendance.objects.filter(course=cr, student=stud).count()
        att_class = Attendance.objects.filter(course=cr, student=stud, status='True').count()
        cta = math.ceil((0.75 * total_class - att_class) / 0.25)
        if cta < 0:
            return 0
        return cta


class AttendanceRange(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()