from django.urls import path

from users.views import RegisterUserView, LoginUserView, profile, GetAllUsersView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('auth/login/', LoginUserView.as_view(), name='login'),
    path('profile/', profile.as_view(), name='granted'),
    path('show/all/', GetAllUsersView.as_view(), name = 'get-all-users')
    ]