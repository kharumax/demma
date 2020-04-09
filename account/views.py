from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.contrib.auth.mixins import (
    LoginRequiredMixin,PermissionRequiredMixin,UserPassesTestMixin
)
from django.views import generic
from django.contrib.auth.views import (LoginView,LogoutView)
from .forms import *
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import Http404, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.conf import settings
User = get_user_model()


class Login(LoginView):
    form_class = LoginForm
    template_name = "account/login.html"


class Logout(LoginRequiredMixin,LogoutView):
    template_name = "product/top.html"


class UserCreate(generic.CreateView):
    template_name = "account/signup.html"
    form_class = SignUpForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()

        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            "protocol": self.request.scheme,
            "domain": domain,
            "token": dumps(user.pk),
            "user": user
        }
        subject = render_to_string("account/mail_template/create/subject.txt",context)
        message = render_to_string("account/mail_template/create/message.txt",context)

        user.email_user(subject,message)
        return redirect("account:signup_done")


class UserCreateDone(generic.TemplateView):
    template_name = "account/signup_done.html"


class UserCreateComplete(generic.TemplateView):
    template_name = "account/signup_complete.html"
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)

    def get(self, request, **kwargs):
        token = kwargs.get("token")
        try:
            user_pk = loads(token,max_age=self.timeout_seconds)
        except SignatureExpired:
            return HttpResponseBadRequest()

        except BadSignature:
            return HttpResponseBadRequest()
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:  # 有効化されていなければ
                    user.activate()
                    user.save()
                    return super().get(request,**kwargs)

        return HttpResponseBadRequest


class MyPage(generic.DetailView):
    model = User
    template_name = "account/my_page.html"






