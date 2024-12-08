# appointments/urls.py
# appointments/urls.py
from django.urls import path
from .views import AppointmentCreateView, AppointmentListView
# AppointmentUpdateView, AppointmentDeleteView, DoctorAppointmentsView, DoctorPatientsView

urlpatterns = [
    path('', AppointmentListView.as_view(), name='appointment-list'),
    path('create/', AppointmentCreateView.as_view(), name='appointment-create'),
    # path('<int:id>/update/', AppointmentUpdateView.as_view(), name='appointment-update'),
    # path('<int:id>/delete/', AppointmentDeleteView.as_view(), name='appointment-delete'),
    # path('doctor/appointments/', DoctorAppointmentsView.as_view(), name='doctor-appointments'),
    # path('doctor/patients/', DoctorPatientsView.as_view(), name='doctor-patients'),
]

