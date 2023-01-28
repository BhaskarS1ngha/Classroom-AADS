from django.urls import path
from . import views

app_name="authentication"

urlpatterns = [
    path("register/",views.register,name="register"),
    path("logout",views.logout_view),
    path("login",views.login_view),
]
