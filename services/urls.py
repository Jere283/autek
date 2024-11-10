from django.urls import path

from services.views import CreateAppointmentView, GetAllAppointmentsView, GetUserAppointmentsView

urlpatterns = [
    path('appointment/show/all/', GetAllAppointmentsView.as_view(), name = 'get-all-appointments'),
    path('appointment/show/<str:user_id>/', GetUserAppointmentsView.as_view(), name = 'get-user-appointments'),
    path('appointment/show/', GetUserAppointmentsView.as_view(), name = 'get-user-appointments-auth'),
    path('appointment/create/one/', CreateAppointmentView.as_view(), name = 'create-appointment')

    ]