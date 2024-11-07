from django.urls import path

from cars.views import GetAllCarsView

urlpatterns = [
    path('show/all/', GetAllCarsView.as_view(), name = 'get-all-cars')
    ]