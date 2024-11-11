from django.urls import path

from cars.views import GetAllCarsView, CreateCarsView, GetUserCarsView

urlpatterns = [
    path('show/all/', GetAllCarsView.as_view(), name = 'get-all-cars'),
    path('create/one/', CreateCarsView.as_view(), name = 'create-all-cars'),
    path('show/<str:user_id>/', GetUserCarsView.as_view(), name='get-user-car'),
    path('show/', GetUserCarsView.as_view(), name='get-user-car-auth'),
]