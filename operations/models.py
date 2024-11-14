from django.db import models
from company.models import *
from files.models import *
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

CURRENCY_CHOICES = (
    ('TL', 'TL'),
    ('USD', 'USD'),
    ('EUR', 'EUR'),
    ('RMB', 'RMB'),
)
SELLCURRENCY_CHOICES = (
    ('TL', 'TL'),
    ('USD', 'USD'),
    ('EUR', 'EUR'),
    ('RMB', 'RMB'),
)

class Operation(models.Model):
    branch = models.ForeignKey(Branch, verbose_name="Branch", related_name="operations", on_delete=models.CASCADE)
    client = models.ForeignKey(Buyercompany, verbose_name=("Buyer Company"), on_delete=models.CASCADE)
    ticket = models.CharField(verbose_name="Ticket", max_length=255)
    follow_employee = models.ForeignKey(Employee, verbose_name="Employee who follows up", related_name="follows", on_delete=models.CASCADE)
    create_employee = models.ForeignKey(Employee, verbose_name="Employee who creates", related_name="creates", on_delete=models.CASCADE)
    start_at = models.DateField(verbose_name="Start At")
    finish_at = models.DateField(verbose_name="Finish At")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(verbose_name="Is Active", default=False)

    def __str__(self):
        return f"Operation {self.ticket} ({self.start_at} - {self.finish_at})"


class Customer(models.Model):
    operation = models.ForeignKey(Operation, verbose_name="Operation", related_name="customers", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Name", max_length=255)
    contact = models.CharField(verbose_name="Contact", max_length=255, blank=True, null=True)
    birthday = models.DateField(verbose_name="Birthday", default="1900-01-01")
    passport = models.CharField(verbose_name="Passport", max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(verbose_name="Is Active", default=False)

    def __str__(self):
        return f"{self.name} ({self.passport})"


class SalesPrice(models.Model):
    operation = models.ForeignKey(Operation, verbose_name="Operation", related_name="sales_prices", on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name="Price", max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=SELLCURRENCY_CHOICES, default='USD')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(verbose_name="Is Active", default=False)

    def __str__(self):
        return f"{self.operation.ticket} - {self.price} {self.currency}"


class OperationDay(models.Model):
    branch = models.ForeignKey(Branch, verbose_name="Branch", related_name="operation_days", on_delete=models.CASCADE)
    operation = models.ForeignKey(Operation, verbose_name="Operation", related_name="operation_days", on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Date")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(verbose_name="Is Active", default=False)

    def __str__(self):
        return f"{self.operation.ticket} - {self.date}"
    
class OperationItem(models.Model):
    operation_day = models.ForeignKey(OperationDay, on_delete=models.CASCADE, related_name="operation_items")
    item_type = models.CharField(max_length=50)
    attributes = models.JSONField(blank=True, null=True)  # Özel alanlar için JSON
    order = models.PositiveIntegerField(blank=True, null=True)  # Sıralama için
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item_type} - Order {self.order}"

class OperationSubItem(models.Model):
    operation_item = models.ForeignKey(OperationItem, on_delete=models.CASCADE, related_name="sub_items")  # ForeignKey ile ilişkilendirildi
    sub_item_type = models.CharField(max_length=50)
    attributes = models.JSONField(blank=True, null=True)
    order = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.sub_item_type} - {self.order}"

