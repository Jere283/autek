from django.urls import path

from services.views import CreateAppointmentView, GetAllAppointmentsView, GetUserAppointmentsView, \
    GetAllAppointmentsStatusView, AppointmentStatusUpdateView, GetAppointmentByIdView, GetWorkshoppAppointmentsView, \
    GetAllServicesView, WorkshopServiceView, CreateAppointmentsImagesView, GetAppointmentByCarIdView, CreateBudgetView, \
    GetBusgetsByAppointmentId, GetBusgetsStatuses, BudgetStatusUpdateView

urlpatterns = [
    path('appointment/show/all/', GetAllAppointmentsView.as_view(), name = 'get-all-appointments'),
    path('appointment/show/user/<str:user_id>/', GetUserAppointmentsView.as_view(), name = 'get-user-appointments'),
    path('appointment/show/workshop/<str:workshop_id>/', GetWorkshoppAppointmentsView.as_view(), name = 'get-workshop-appointments'),
    path('appointment/show/<int:id>/', GetAppointmentByIdView.as_view(), name = 'get-appointments-by-id'),
    path('appointment/show/car/<int:id>/', GetAppointmentByCarIdView.as_view(), name = 'get-appointments-by-id'),
    path('appointment/show/', GetUserAppointmentsView.as_view(), name = 'get-user-appointments-auth'),
    path('appointment/create/one/', CreateAppointmentView.as_view(), name = 'create-appointment'),
    path('appointment/image/add/', CreateAppointmentsImagesView.as_view(), name = 'add_appointment_image'),

    # Statuses
    path('appointment/status/show/all/', GetAllAppointmentsStatusView.as_view(), name = 'get-appointments-status'),
    path('appointment/<str:appointment_id>/status/update/', AppointmentStatusUpdateView.as_view(), name='update-appointment-status'),

    # Services
    path('show/all/', GetAllServicesView.as_view(), name='get-all-services'),
    path('workshop/show/all/', WorkshopServiceView.as_view(), name='get-all-services-from-workshops'),

    # Budget
    path('appointment/budget/new/', CreateBudgetView.as_view(), name = 'create-budget'),
    path('appointment/<int:id>/budget/show/', GetBusgetsByAppointmentId.as_view(), name = 'get-budgets-id'),
    path('budget/status/show/', GetBusgetsStatuses.as_view(), name = 'get-budgets-status'),
    path('budget/<int:id>/status/update/', BudgetStatusUpdateView.as_view(),name='update-budget-status'),

]