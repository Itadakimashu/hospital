from django.shortcuts import redirect,get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView,DeleteView,UpdateView,TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import AppointmentForm,AppointmentEditForm
from .models import Appointment

from doctor.models import Doctor
from paitent.models import Paitent

# Create your views here.

class MakeAppointmentView(LoginRequiredMixin,CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointment/make_appointment.html'
    success_url = reverse_lazy('appointment_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        doctor = get_object_or_404(Doctor, id=self.kwargs['id'])
        kwargs['doctor'] = doctor
        return kwargs

    def form_valid(self,form):
        doctor = Doctor.objects.get(id=self.kwargs['id'])
        paitent = Paitent.objects.get(user=self.request.user)
        form.instance.doctor = doctor
        form.instance.paitent = paitent
        return super().form_valid(form)
    
class AppointmentListView(LoginRequiredMixin,ListView):
    model = Appointment
    template_name = 'appointment/appointment_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paitent = Paitent.objects.get(user=self.request.user)
        context['appointment_list'] = Appointment.objects.filter(paitent=paitent)
        return context
    

class CancelAppointmentView(LoginRequiredMixin,TemplateView):
    model = Appointment
    template_name = 'appointment/cancel_appointment.html'
    success_url = reverse_lazy('appointment_list')
    pk_url_kwarg = 'id'

    def post(self, request, *args, **kwargs):
        appointment = get_object_or_404(Appointment, pk=kwargs.get(self.pk_url_kwarg))
        appointment.status = 'cancelled'
        appointment.save()
        return redirect(self.success_url)
    
class EditAppointmentView(LoginRequiredMixin,UpdateView):
    model = Appointment
    form_class = AppointmentEditForm
    template_name = 'appointment/edit_appointment.html'
    success_url = reverse_lazy('doctor_profile')
    pk_url_kwarg = 'id'


class AppointmentDeleteView(LoginRequiredMixin,DeleteView):
    model = Appointment
    template_name = 'appointment/delete_appointment.html'
    success_url = reverse_lazy('doctor_profile')
    pk_url_kwarg = 'id'
    

