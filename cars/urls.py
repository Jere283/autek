from django.urls import path

from cars.views import GetAllCarsView, CreateCarsView, GetUserCarsView, GetAllCarsColors, GetAllCarsBrands, \
    GetAllCarsModels

urlpatterns = [
    path('show/all/', GetAllCarsView.as_view(), name = 'get-all-cars'),
    path('show/all/colors/', GetAllCarsColors.as_view(), name = 'get-all-colors'),
    path('show/all/brands/', GetAllCarsBrands.as_view(), name = 'get-all-brands'),
    path('show/all/brands/<int:brand_id>/model/', GetAllCarsModels.as_view(), name = 'get-all-models'),
    path('create/one/', CreateCarsView.as_view(), name = 'create-all-cars'),
    path('show/user/<str:user_id>/', GetUserCarsView.as_view(), name='get-user-car'),
    path('show/<int:id>/', GetAllCarsView.as_view(), name='get-user-car'),
    path('show/', GetUserCarsView.as_view(), name='get-user-car-auth'),
]