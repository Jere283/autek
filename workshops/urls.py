from django.urls import path

from workshops.views import GetWorkshopsView

urlpatterns = [
    path('show/all/', GetWorkshopsView.as_view(), name = 'get-all-workshops'),
    path('show/<str:workshop_id>/', GetWorkshopsView.as_view(), name = 'get-workshop-id'),


    ]