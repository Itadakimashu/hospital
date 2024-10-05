from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Paitent

class PaitentCreateForm(UserCreationForm):
    age = forms.IntegerField(required=True)
    phone = forms.CharField(max_length=12, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields =  ('username', 'password1','password2','first_name', 'last_name', 'email','age','phone')

    def save(self,commit=True):
        user = super().save(commit=False)
        if commit:
            user.is_active = False
            user.save()

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            confirm_link = f'https://final-exam-l68w.onrender.com/paitent/active/{uid}/{token}'
            
            email_subject = 'Confirm Your Email'
            email_body = render_to_string('paitent/confirm_email.html',{'confirm_link':confirm_link})

            email = EmailMultiAlternatives(email_subject,'',to = [user.email])
            email.attach_alternative(email_body,'text/html')
            email.send()

            age = self.cleaned_data['age']
            phone = self.cleaned_data['phone']
            Paitent.objects.create(user=user,age=age,phone=phone)
            return user
    
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('User with this Email Exists!')
        
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return phone
    


class PaitentUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True) 

    class Meta:
        model = Paitent
        fields = ['phone', 'age']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['username'].initial = user.username
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

    def save(self, commit=True):
        patient = super().save(commit=False)
        user = patient.user
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            patient.save()
        return patient
        