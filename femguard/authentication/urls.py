from django.urls import path
from .views import (
    user_register,
    user_login,
    admin_login,
    user_logout,
    get_current_user,
    get_csrf_token
)

urlpatterns = [
    path('register', user_register, name='register'),
    path('user_login', user_login, name='user_login'),
    path('admin_login', admin_login, name='admin_login'),
    path('logout', user_logout, name='logout'),
    path('me', get_current_user, name='get_current_user'),
    path('csrf_token/', get_csrf_token, name='csrf_token'),
]
