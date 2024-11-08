# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('files/<str:model>/', generic_view, name='generic_view'),
    path('files/<str:model>/create/', generic_create_view, name='generic_create_view'),
    path('files/<str:model>/edit/<int:obj_id>/', generic_edit_view, name='generic_edit_view'),
    path('files/<str:model>/delete/<int:obj_id>/', generic_delete_view, name='generic_delete_view'),
    path('files/<str:model>/cancel/<int:obj_id>/', generic_cancel_view, name='generic_cancel_view'),
    path('files/<str:model>/reload/<int:obj_id>/', generic_reload_view, name='generic_reload_view'),
]
