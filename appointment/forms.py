from typing import Any
from django import forms
from .models import Appointment
from doctor.models import Doctor,AvailableTime

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['time', 'symptoms', 'type']
        labels = {
            'doctor': 'Select Doctor',
            'paitent': 'Select Patient',
            'time': 'Select Time Slot',
            'symptoms': 'Describe Symptoms',
            'type': 'Appointment Type',
        }

    def __init__(self,*args,**kwargs):
        doctor = kwargs.pop('doctor', None) 
        super(AppointmentForm, self).__init__(*args, **kwargs)
        if doctor:
            self.fields['time'].queryset = AvailableTime.objects.filter(doctor=doctor)

class AppointmentEditForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['time','status','doctor_review']

    def __init__(self,*args,**kwargs):
        super(AppointmentEditForm, self).__init__(*args, **kwargs)
        doctor = self.instance.doctor
        self.fields['time'].queryset = doctor.available_time

    def save(self, commit=True):
        instance = super(AppointmentEditForm, self).save(commit=False)
        if commit:
            instance.save()
            if instance.status == 'running':
                meet_link = instance.doctor.meet_link
                
                email_subject = 'Join the meet link'
                email_body = render_to_string('appointment/meet_link_email.html',{'meet_link':meet_link})

                email = EmailMultiAlternatives(email_subject,'',to = [instance.paitent.user.email])
                email.attach_alternative(email_body,'text/html')
                email.send()
            return instance



