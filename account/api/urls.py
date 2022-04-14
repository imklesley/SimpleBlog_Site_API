from django.urls import path

from .views import api_register_account_view, api_login_account_view

from rest_framework.authtoken.views import obtain_auth_token

app_name = 'account_api'

urlpatterns = [
    path('register/', api_register_account_view, name='register'),
    path('login-obtain-auth-token/', obtain_auth_token, name='login-obtain-auth-token'),
    path('login/', api_login_account_view, name='login'),
]
