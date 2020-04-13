from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.models import User
from django.shortcuts import redirect, HttpResponseRedirect
from django.contrib import messages

from . import forms

class LoginView(generic.FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('instructor:instructor')
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        # direct a user if authenticated
        if request.user.is_authenticated and request.user.is_student:
            return HttpResponseRedirect(reverse_lazy('student:student'))
        elif request.user.is_authenticated and request.user.is_student == False:
            return HttpResponseRedirect(reverse_lazy('instructor:instructor'))
        return super(LoginView, self).get(request, *args, **kwargs)
    
    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request, **self.get_form_kwargs())
      
    def form_valid(self, form):
        if form.data['account'] == 'student':
            self.success_url = reverse_lazy('student:student')

        login(self.request, form.get_user())
        return super().form_valid(form)
    
    def form_invalid(self, form):
        if form.data['account'] == 'student':
            self.success_url = reverse_lazy('student:student')

        messages.error(self.request, 'Username or password is wrong')
        return super().form_valid(form)

class SignUpView(generic.CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('instructor:instructor')
    template_name = "accounts/signup.html"

    def form_valid(self, form):
        form = forms.UserCreateForm(self.request.POST.copy())
        try:
            if self.request.POST['accountSU'] == 'studentSU':
                form.data['is_student'] = 'on'
                self.success_url = reverse_lazy('student:student')
        except:
            return super().form_valid(form)

        return super().form_valid(form)

class LogoutView(generic.RedirectView):
    url = reverse_lazy('accounts:login')
    
    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)