from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm

User = get_user_model()


class LoginForm(AuthenticationForm):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = field.label


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("email","name",)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def clean_email(self):
        email = self.cleaned_data["email"]
        User.objects.filter(email=email,is_active=False).delete()
        return email


