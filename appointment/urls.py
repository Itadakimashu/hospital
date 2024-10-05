from django.urls import path

from .views import (
    MakeAppointmentView,
    AppointmentListView,
    CancelAppointmentView,
    EditAppointmentView,
    AppointmentDeleteView
)

urlpatterns = [
    path('list/',AppointmentListView.as_view(),name='appointment_list'),
    path('cancel/<int:id>/',CancelAppointmentView.as_view(),name = 'cancel_appointment'),
    path('make_appointment/<int:id>/',MakeAppointmentView.as_view(),name='make_appointment'),
    path('edit/<int:id>/',EditAppointmentView.as_view(),name = 'edit_appointment'),
    path('delete/<int:id>/',AppointmentDeleteView.as_view(),name = 'delete_appointment'),
]
