from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView,UpdateView

from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode

from rest_framework import viewsets

from .models import Paitent
from .serializers import PaitentSerializer

from .forms import PaitentCreateForm,PaitentUpdateForm

# Create your views here.
class PaitentRegisterView(CreateView):
    model = Paitent
    form_class = PaitentCreateForm
    template_name = 'paitent/signup.html'
    success_url = reverse_lazy('signup')

    
class PaitentProfileView(LoginRequiredMixin, UpdateView):
    model = Paitent
    form_class = PaitentUpdateForm
    template_name = 'paitent/profile.html'
    success_url = reverse_lazy('paitent_profile')  

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_object(self):
        return get_object_or_404(Paitent, user=self.request.user)

    


def activate(request,uid64,token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if user.is_active:
            return HttpResponse('Account already activated')
        user.is_active = True
        user.save()
        return redirect('login')
    
    else:
        return redirect('signup')

class PaitentViewSet(viewsets.ModelViewSet):
    queryset = Paitent.objects.all()
    serializer_class = PaitentSerializer
    