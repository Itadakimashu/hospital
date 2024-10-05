from django.shortcuts import render
from django.urls import reverse_lazy
from rest_framework import viewsets

from django.views.generic import DetailView,CreateView,TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Doctor,Specialization,AvailableTime,Designation
from .forms import ReviewForm,DoctorCreationForm
from .serializers import DoctorSerializer,SpecializationSerializer,AvailableTimeSerializer,DesignationSerializer

from paitent.models import Paitent
from appointment.models import Appointment

# Create your views here.

class DoctorDetailsView(DetailView,CreateView):
    model = Doctor
    template_name = 'doctor/details.html'
    pk_url_kwarg = 'id'
    form_class = ReviewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = Doctor.objects.get(id=self.kwargs['id'])

        has_appointment = False
        if self.request.user.is_authenticated and self.request.session['role'] == 'paitent':
            paitent = Paitent.objects.get(user=self.request.user)
            if paitent.appointments.filter(doctor=doctor).exists():
                has_appointment = True

        context['has_appointment'] = has_appointment

        return context

    def get_success_url(self):
        return reverse_lazy('doctor_details',kwargs={'id':self.get_object().id})

    def form_valid(self,form):
        form.instance.doctor = self.get_object()
        form.instance.paitent = Paitent.objects.get(user=self.request.user)
        return super().form_valid(form)
    

class DoctorProfileView(LoginRequiredMixin,TemplateView):
    template_name = 'doctor/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = Doctor.objects.get(user=self.request.user)
        context['doctor'] = doctor
        context['appointments'] = Appointment.objects.filter(doctor=doctor)
        return context
    

class DoctorRegisterView(CreateView):
    model = Doctor
    form_class = DoctorCreationForm
    template_name = 'doctor/signup.html'
    success_url = reverse_lazy('login')

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer

class AvailableTimeViewSet(viewsets.ModelViewSet):
    queryset = AvailableTime.objects.all()
    serializer_class = AvailableTimeSerializer

class DesignationViewSet(viewsets.ModelViewSet):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer



    

