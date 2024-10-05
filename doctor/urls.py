from django.urls import path
from . import views
urlpatterns = [
    path('details/<int:id>/',views.DoctorDetailsView.as_view(), name='doctor_details'),
    path('profile/',views.DoctorProfileView.as_view(),name = 'doctor_profile'),
    path('register/',views.DoctorRegisterView.as_view(),name = 'doctor_signup'),
]
