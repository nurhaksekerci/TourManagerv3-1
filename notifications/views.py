from django.shortcuts import render
from django.http import JsonResponse
from django.utils.timezone import now
from .models import *
from django.http import HttpResponse

def unread_count(request):
    employee = Employee.objects.get(user=request.user)
    count = NotificationDetail.objects.filter(employee=employee, read_at__isnull=True, is_delete=False).count()
    last_count = request.session.get('last_unread_count', 0)

    content_changed = count != last_count
    request.session['last_unread_count'] = count  # Durumu güncelleyin

    # Sadece sayıyı döndür
    return JsonResponse({"count": count, "content_changed": content_changed})


def notifications(request):
    employee = Employee.objects.get(user=request.user)
    notifications = NotificationDetail.objects.filter(
        employee=employee, 
        is_delete=False
    ).order_by('-notification__created_at')[:10]  # En yeni bildirimleri getir
    return render(request, 'main/includes/notifications.html', {'notifications': notifications})



def mark_as_read(request, notification_id):
    employee = Employee.objects.get(user=request.user)
    detail = NotificationDetail.objects.get(notification_id=notification_id, employee=employee)
    detail.read_at = now()
    detail.save()
    return HttpResponse("Read")


def delete_notification(request, notification_id):
    try:
        employee = Employee.objects.get(user=request.user)
        detail = NotificationDetail.objects.get(notification_id=notification_id, employee=employee)
        detail.is_delete = True
        if detail.read_at is None:  # Eğer bildirim okunmamışsa, okunma zamanını şimdi olarak ayarla
            detail.read_at = now()
        detail.delete_at = now()
        detail.save()
        return HttpResponse(status=200)
    except NotificationDetail.DoesNotExist:
        return JsonResponse({"success": False, "error": "Notification not found"}, status=404)





def mark_all_as_read(request):
    employee = Employee.objects.get(user=request.user)
    NotificationDetail.objects.filter(employee=employee, read_at__isnull=True).update(read_at=now())
    return JsonResponse({"success": True})


from django.shortcuts import render
from .models import NotificationDetail

def all_notifications(request):
    employee = Employee.objects.get(user=request.user)
    notifications = NotificationDetail.objects.filter(employee=employee).select_related('notification')
    return render(request, 'notifications/all_notifications.html', {'notifications': notifications})
