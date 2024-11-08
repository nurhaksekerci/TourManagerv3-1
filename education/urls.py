from django.urls import path
from . import views

urlpatterns = [
    path('egitim-plan/', views.egitim_plan_view, name='egitim_plan'),
    path('get-available-days/', views.get_available_days, name='get_available_days'),
]
