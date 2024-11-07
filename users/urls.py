from django.urls import path

from users.views import RegisterUserView, LoginUserView, profile

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('profile/', profile.as_view(), name='granted'),
    ]