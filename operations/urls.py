from django.urls import path
from .views import *

urlpatterns = [
    path('create/', operation_create, name='operation_create'),
    path('create-operation-item/<int:day_id>/', create_item_detail, name='create_item_detail'),
    path('create-operation-item/<int:day_id>/<str:item_type>/<str:item_no>/', create_items, name='create_operation_item'),
    path('create-operation-item/<int:day_id>/<str:item_type>/<str:item_no>/<str:sub_item_type>/<str:sub_item_no>/', create_sub_items, name='create_sub_items'),
    path('save-operation-item/<int:day_id>/', save_all_forms, name='save_all_forms'),
]

