from django.urls import path
from .views import *

app_name = "product"
urlpatterns = [
    path('',Top.as_view(),name="top"),
]