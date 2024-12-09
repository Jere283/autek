from django.urls import path

from services.views import CreateAppointmentView, GetAllAppointmentsView, GetUserAppointmentsView, \
    GetAllAppointmentsStatusView, AppointmentStatusUpdateView, GetAppointmentByIdView, GetWorkshoppAppointmentsView

urlpatterns = [
    path('appointment/show/all/', GetAllAppointmentsView.as_view(), name = 'get-all-appointments'),
    path('appointment/show/user/<str:user_id>/', GetUserAppointmentsView.as_view(), name = 'get-user-appointments'),
    path('appointment/show/workshop/<str:workshop_id>/', GetWorkshoppAppointmentsView.as_view(), name = 'get-workshop-appointments'),
    path('appointment/show/<int:id>/', GetAppointmentByIdView.as_view(), name = 'get-appointments-by-id'),
    path('appointment/show/', GetUserAppointmentsView.as_view(), name = 'get-user-appointments-auth'),
    path('appointment/create/one/', CreateAppointmentView.as_view(), name = 'create-appointment'),
    path('appointment/status/show/all/', GetAllAppointmentsStatusView.as_view(), name = 'get-appointments-status'),

    path('appointment/<str:appointment_id>/status/update/', AppointmentStatusUpdateView.as_view(), name='update-appointment-status'),


    ]