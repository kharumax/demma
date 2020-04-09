from django.urls import path
from .views import *

app_name = "account"
urlpatterns = [
    path('login/',Login.as_view(),name="login"),
    path('logout/',Logout.as_view(),name="logout"),
    path('signup/',UserCreate.as_view(),name="signup"),
    path('signup/done/',UserCreateDone.as_view(),name="signup_done"),
    path('signup/complete/<token>/',UserCreateComplete.as_view(),name="signup_complete"),

]




