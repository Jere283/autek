from django.urls import path

from cars.views import GetAllCarsView, CreateCarsView

urlpatterns = [
    path('show/all/', GetAllCarsView.as_view(), name = 'get-all-cars'),
    path('create/one/', CreateCarsView.as_view(), name = 'create-all-cars')
    ]