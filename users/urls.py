from django.urls import path

from users.views import RegisterUserView, LoginUserView, profile, GetAllUsersView, LogoutApiView, GetAllRoles, TestToken

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('auth/login/', LoginUserView.as_view(), name='login'),
    path('auth/logout/', LogoutApiView.as_view(), name='logout'),
    path('auth/test/', TestToken.as_view(), name='test'),
    path('profile/', profile.as_view(), name='granted'),
    path('show/all/', GetAllUsersView.as_view(), name = 'get-all-users'),

    #admin
    path('roles/show/all/', GetAllRoles.as_view(), name = 'get-all-roles')
    ]