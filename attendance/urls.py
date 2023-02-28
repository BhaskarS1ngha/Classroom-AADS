from django.urls import path
from . import views

app_name="attendance"

urlpatterns = [
    path("create_attendance/<slug:class_code>/",views.create_attendance,name="create_attendance"),
    path("confirm/<int:attendance_id>/",views.confirm,name="confirm"),
    ]