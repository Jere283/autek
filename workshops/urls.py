from django.urls import path

from workshops.views import GetWorkshopsView, GetWorkshopsByIdView

urlpatterns = [
    path('show/all/', GetWorkshopsView.as_view(), name = 'get-all-workshops'),
    path('show/<str:workshop_id>/', GetWorkshopsByIdView.as_view(), name = 'get-workshop-id'),


    ]