from django.db import models
from company.models import *


class Notification(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications')  # Şube ilişkisi
    created_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='created_notifications')
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    recipients = models.ManyToManyField(Employee, related_name='notifications')

    def __str__(self):
        return self.title

class NotificationDetail(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='details')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='notification_details')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='notification_details')  # Şube ilişkisi
    read_at = models.DateTimeField(null=True, blank=True)
    delete_at = models.DateTimeField(null=True, blank=True)
    is_delete = models.BooleanField(verbose_name=("Is active"), default=False)

    def __str__(self):
        return f"NotificationDetail for {self.employee.user.username}"
