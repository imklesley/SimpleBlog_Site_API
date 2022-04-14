from django.urls import path
from django.contrib.auth import views as auth_views

from account.views import registration_view, logout_view, login_view, account_view, must_authenticate_view

urlpatterns = [
    path('register/', registration_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('account/', account_view, name='account'),
    path('must_authenticate/', must_authenticate_view, name='must_authenticate'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='account/password_change.html'),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'),
         name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='account/password_reset_form.html',
                                                                 email_template_name='account/password_reset_email.html'
                                                                 ,
                                                                 subject_template_name='account/password_reset_subject.txt'),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'),
         name='password_reset_complete'),

]
