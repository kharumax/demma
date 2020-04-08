from django.shortcuts import render,redirect,resolve_url
from .models import *
from django.contrib.auth import get_user_model
from django.views import generic

User = get_user_model()


class Top(generic.TemplateView):
    template_name = "product/top.html"
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()
        context["products"] = products
        return context






