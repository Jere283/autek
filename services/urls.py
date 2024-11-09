from django.urls import path

from services.views import CreateAppointmentView, GetAllAppointmentsView

urlpatterns = [
    path('appointment/show/all/', GetAllAppointmentsView.as_view(), name = 'get-all-appointments'),
    path('appointment/create/one/', CreateAppointmentView.as_view(), name = 'create-appointment')
    ]