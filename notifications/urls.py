from django.urls import path
from . import views

urlpatterns = [
    # Okunmamış bildirim sayısını döndüren endpoint
    path('unread-count/', views.unread_count, name='unread_count'),
    
    # Bildirim listesini döndüren endpoint
    path('', views.notifications, name='notifications'),
    
    # Belirli bir bildirimi okundu olarak işaretleme
    path('<int:notification_id>/mark-as-read/', views.mark_as_read, name='mark_as_read'),
    
    # Belirli bir bildirimi silme
    path('<int:notification_id>/delete/', views.delete_notification, name='delete_notification'),
    
    # Tüm bildirimleri okundu olarak işaretleme
    path('mark-all-as-read/', views.mark_all_as_read, name='mark_all_as_read'),
    
    # Tüm bildirimleri listeleyen genel bir sayfa (isteğe bağlı)
    path('all/', views.all_notifications, name='all_notifications'),
]
