from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView,LogoutView

from doctor.models import Doctor
from paitent.models import Paitent

class UserLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('home')
    
    def form_valid(self, form):

        response = super().form_valid(form)

        user = self.request.user

        if Doctor.objects.filter(user=user).exists():
            self.request.session['role'] = 'doctor'
        elif Paitent.objects.filter(user=user).exists():
            self.request.session['role'] = 'paitent'
        else:
            self.request.session['role'] = 'unknown'

        return response
    

class UserLogoutView(LogoutView):
    def get_success_url(self):
        return reverse_lazy('home')