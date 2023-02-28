from django.urls import path
from . import views

app_name="attendance"

urlpatterns = [
    # path("create_attendance/<slug:class_code>/",views.create_attendance,name="create_attendance"),
    # path("confirm/<int:attendance_id>/",views.confirm,name="confirm"),
    path("view_attendance/<slug:class_code>/<int:student_id>/",views.view_attendance,name="view_attendance"),
    path("new_attendance/<slug:class_code>/",views.new_attendance,name="new_attendance"),
    path("confirm/<slug:class_code>/",views.confirm,name="confirm_new"),
    ]