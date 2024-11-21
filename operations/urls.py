from django.urls import path
from .views import *

urlpatterns = [
    path('jobs/', jobs, name='jobs'),
    path('create/', operation_create, name='operation_create'),
    path('create-operation-item/<int:day_id>/', create_item_detail, name='create_item_detail'),
    path('create-operation-item/<int:day_id>/<str:item_type>/<str:item_no>/', create_items, name='create_operation_item'),
    path('create-operation-item/<int:day_id>/<str:item_type>/<str:item_no>/<str:sub_item_type>/<str:sub_item_no>/', create_sub_items, name='create_sub_items'),
    path('save-operation-item/<int:day_id>/', save_all_forms, name='save_all_forms'),
    path('operation_item/update/<int:pk>/<str:item_type>/', update_operation_item, name='update_operation_item'),
    path('operation_sub_item/update/<int:pk>/<str:sub_item_type>/', update_operation_sub_item, name='update_operation_sub_item'),

]

