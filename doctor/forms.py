from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Review,Doctor,AvailableTime,Designation, Specialization

    

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rate', 'review')


class DoctorCreationForm(forms.ModelForm):
    # User fields
    username = forms.CharField(max_length=150, required=True, label='Username')
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='Password')
    first_name = forms.CharField(max_length=30, required=True, label='First Name')
    last_name = forms.CharField(max_length=30, required=True, label='Last Name')
    email = forms.EmailField(max_length=254, required=True, label='Email')

    # Doctor fields
    image = forms.ImageField(required=True, label='Profile Image')
    designation = forms.ModelChoiceField(queryset=Designation.objects.all(), required=True, label='Designation')
    specialization = forms.ModelMultipleChoiceField(queryset=Specialization.objects.all(), required=True, widget=forms.CheckboxSelectMultiple, label='Specialization')
    available_time = forms.ModelMultipleChoiceField(queryset=AvailableTime.objects.all(), required=True, widget=forms.CheckboxSelectMultiple, label='Available Time')
    fee = forms.DecimalField(max_digits=10, decimal_places=2, required=True, label='Fee')
    meet_link = forms.URLField(required=False, label='Meeting Link')

    class Meta:
        model = Doctor
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'image', 'designation', 'specialization', 'available_time', 'fee', 'meet_link']

    def save(self, commit=True):
        # Save the user instance
        user = User(
            username=self.cleaned_data['username'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email']
        )
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()

        # Save the doctor instance
        doctor = super().save(commit=False)
        doctor.user = user
        if commit:
            doctor.save()
            self.save_m2m()  # Save ManyToMany relationships (specialization and available_time)

        return doctor