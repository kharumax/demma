from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.mixins import (
    LoginRequiredMixin,PermissionRequiredMixin,UserPassesTestMixin
)
from django.views import generic
from django.contrib.auth.views import (LoginView,LogoutView)
from .forms import *


class Login(LoginView):
    form_class = LoginForm
    template_name = "account/login.html"


class Logout(LoginRequiredMixin,LogoutView):
    template_name = "product/top.html"

