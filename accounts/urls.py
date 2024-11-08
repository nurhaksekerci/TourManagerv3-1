# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('login/', auth_login, name='auth_login'),
    path('register/company/', auth_company_register, name='auth_company_register'),
    path('ajax/load-districts/', load_districts, name='ajax_load_districts'),
    path('ajax/load-neighborhoods/', load_neighborhoods, name='ajax_load_neighborhoods'),
    path('register/company/<slug:slug>/register/employee', auth_employee_register, name='auth_employee_register'),
    path('email/verify/<slug:slug>/', verify_email, name='aut_email_verify'),
    path('password-reset/', auth_password_reset_request, name='auth_password_reset_request'),
    path('password-reset/<uidb64>/<token>/', auth_password_reset_confirm, name='auth_password_reset_confirm'),
    path('password-reset/send-mail/', send_mail_reset_password, name='send_mail_reset_password'),
    path('phone/verify/<str:phone>/', auth_phone_verify, name='auth_phone_verify'),
    path('profile/<slug:slug>/', profile, name='profile'),
    path('my-profile/', profile, name='my_profile'),
]
