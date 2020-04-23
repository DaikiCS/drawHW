from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views import generic
from . import mixins

class TestView(mixins.StudentRequiredMixin, generic.TemplateView):
    template_name = 'student/home.html'
