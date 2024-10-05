from django.urls import path

from . import views

urlpatterns = [
    path('register/',views.PaitentRegisterView.as_view(), name='signup'),
    path('profile/',views.PaitentProfileView.as_view(),name='paitent_profile'),
    path('active/<uid64>/<token>/',views.activate, name='activate'),
]
