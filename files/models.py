from django.db import models
from company.models import *

CURRENCY_CHOICES = (
    ('TL', 'TL'),
    ('USD', 'USD'),
    ('EUR', 'EUR'),
    ('RMB', 'RMB'),
)

class Vehicle(models.Model):
    branch=models.ForeignKey(Branch, verbose_name="Branch", on_delete=models.CASCADE)
    vehicle = models.CharField(verbose_name="Vehicle", max_length=155)
    capacity = models.PositiveIntegerField(verbose_name="Capacity")
    created_at = models.DateField(verbose_name="Created At", auto_now_add=True)
    updated_at = models.DateField(verbose_name="Last Updated At", auto_now=True)
    is_delete =  models.BooleanField(verbose_name="Is Active", default=False)

    def __str__(self):
        return self.vehicle

class NoVehicleTour(models.Model):
    branch=models.ForeignKey(Branch, verbose_name="Branch", on_delete=models.CASCADE)
    route = models.CharField(verbose_name="Route", max_length=155)
    city = models.ForeignKey(City, verbose_name="Start City", on_delete=models.CASCADE, related_name="cities")
    created_at = models.DateField(verbose_name="Created At", auto_now_add=True)
    updated_at = models.DateField(verbose_name="Last Updated At", auto_now=True)
    is_delete =  models.BooleanField(verbose_name="Is Active", default=False)

    def __str__(self):
        return self.route
    
class Tour(models.Model):
    branch=models.ForeignKey(Branch, verbose_name="Branch", on_delete=models.CASCADE)
    route = models.CharField(verbose_name="Route", max_length=155)
    start_city = models.ForeignKey(City, verbose_name="Start City", on_delete=models.CASCADE, related_name="tourstartcities")
    finish_city = models.ForeignKey(City, verbose_name="Finish City", on_delete=models.CASCADE, related_name="tourfinishcities")
    created_at = models.DateField(verbose_name="Created At", auto_now_add=True)
    updated_at = models.DateField(verbose_name="Last Updated At", auto_now=True)
    is_delete =  models.BooleanField(verbose_name="Is Active", default=False)

    def __str__(self):
        return self.route

class Transfer(models.Model):
    branch=models.ForeignKey(Branch, verbose_name="Branch", on_delete=models.CASCADE)
    route = models.CharField(verbose_name="Route", max_length=155)
    start_city = models.ForeignKey(City, verbose_name="Start City", on_delete=models.CASCADE, related_name="transferstartcities")
    finish_city = models.ForeignKey(City, verbose_name="Finish City", on_delete=models.CASCADE, related_name="transferfinishcities")
    created_at = models.DateField(verbose_name="Created At", auto_now_add=True)
    updated_at = models.DateField(verbose_name="Last Updated At", auto_now=True)
    is_delete =  models.BooleanField(verbose_name="Is Active", default=False)

    def __str__(self):
        return self.route
    

class Hotel(models.Model):
    branch=models.ForeignKey(Branch, verbose_name="Branch", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Name", max_length=100)
    location = models.ForeignKey(City, verbose_name="Location", on_delete=models.CASCADE, blank=True, null=True)
    mail = models.CharField(verbose_name="Email", max_length=155, blank=True, null=True)
    one_person = models.DecimalField(verbose_name="Tek Kişilik Price", max_digits=10, decimal_places=2, default=0)
    two_person = models.DecimalField(verbose_name="İki Kişilik Price", max_digits=10, decimal_places=2, default=0)
    tree_person = models.DecimalField(verbose_name="Üç Kişilik Price", max_digits=10, decimal_places=2, default=0)
    finish = models.DateField(verbose_name="Price Geçerlilik Tarihi", blank=True, null=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, verbose_name="Currency", default="TL")
    created_at = models.DateField(verbose_name="Created At", auto_now_add=True)
    updated_at = models.DateField(verbose_name="Last Updated At", auto_now=True)
    is_delete =  models.BooleanField(verbose_name="Is Active", default=False)

    def __str__(self):
        return f"{self.name} - {self.location}"

class Activity(models.Model):
    branch=models.ForeignKey(Branch, verbose_name="Branch", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Name", max_length=100)
    location = models.ManyToManyField(City, verbose_name="Location")
    created_at = models.DateField(verbose_name="Created At", auto_now_add=True)
    updated_at = models.DateField(verbose_name="Last Updated At", auto_now=True)
    is_delete =  models.BooleanField(verbose_name="Is Active", default=False)

    def __str__(self):
        return f"{self.location} - {self.name}"

class Museum(models.Model):
    branch=models.ForeignKey(Branch, verbose_name="Branch", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Name", max_length=100)
    location = models.ForeignKey(City, verbose_name="Location", on_delete=models.CASCADE, blank=True, null=True)
    contact = models.CharField(verbose_name="Contact", max_length=155, blank=True, null=True)
    price = models.DecimalField(verbose_name="Price", max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, verbose_name="Currency", default="TL")
    created_at = models.DateField(verbose_name="Created At", auto_now_add=True)
    updated_at = models.DateField(verbose_name="Last Updated At", auto_now=True)
    is_delete =  models.BooleanField(verbose_name="Is Active", default=False)

    def __str__(self):
        return f"{self.location} - {self.name}"
    
class Guide(models.Model):
    branch=models.ForeignKey(Branch, verbose_name="Branch", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Name", max_length=155)
    location = models.ManyToManyField(City, verbose_name="Location")
    doc_no = models.CharField(verbose_name="Guide No", max_length=155, blank=True, null=True)
    phone = models.CharField(verbose_name="Phone", max_length=155)
    mail = models.CharField(verbose_name="Email", max_length=155, blank=True, null=True)
    price = models.DecimalField(verbose_name="Price", max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, verbose_name="Currency", default="TL")
    created_at = models.DateField(verbose_name="Created At", auto_now_add=True)
    updated_at = models.DateField(verbose_name="Last Updated At", auto_now=True)
    is_delete =  models.BooleanField(verbose_name="Is Active", default=False)

    def __str__(self):
        return f"{self.location} - {self.name}"
    
class VehicleSupplier(models.Model):
    branch=models.ForeignKey(Branch, verbose_name="Branch", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Name", max_length=100)
    location = models.ManyToManyField(City, verbose_name="Location")
    contact = models.CharField(verbose_name="Contact", max_length=155)
    created_at = models.DateField(verbose_name="Created At", auto_now_add=True)
    updated_at = models.DateField(verbose_name="Last Updated At", auto_now=True)
    is_delete =  models.BooleanField(verbose_name="Is Active", default=False)

    def __str__(self):
        return f"{self.name}"
    
class Activitysupplier(models.Model):
    branch=models.ForeignKey(Branch, verbose_name="Branch", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Name", max_length=100)
    location = models.ManyToManyField(City, verbose_name="Location")
    contact = models.CharField(verbose_name="Contact", max_length=155)
    created_at = models.DateField(verbose_name="Created At", auto_now_add=True)
    updated_at = models.DateField(verbose_name="Last Updated At", auto_now=True)
    is_delete =  models.BooleanField(verbose_name="Is Active", default=False)

    def __str__(self):
        return f"{self.name}"
    
class Vehiclecost(models.Model):
    branch=models.ForeignKey(Branch, verbose_name="Branch", on_delete=models.CASCADE)
    supplier = models.ForeignKey(VehicleSupplier, verbose_name="Supplier", on_delete=models.CASCADE)
    tour=models.ForeignKey(Tour, verbose_name="Tour", on_delete=models.CASCADE, blank=True, null=True)
    transfer=models.ForeignKey(Transfer, verbose_name="Transfer", on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateField(verbose_name="Created At", auto_now_add=True)
    updated_at = models.DateField(verbose_name="Last Updated At", auto_now=True)
    is_delete =  models.BooleanField(verbose_name="Is Active", default=False)

    def __str__(self):
        if self.tour:
            return f"{self.supplier.name} - {self.tour}"
        else:
            return f"{self.supplier.name} - {self.transfer}"
    
class VehicleCostPrice(models.Model):
    vehicle_cost = models.ForeignKey(Vehiclecost, verbose_name="Vehicle Cost", on_delete=models.CASCADE, related_name="vehiclecostprices")
    vehicle = models.ForeignKey(Vehicle, verbose_name="Vehicle", on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name="Price", max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, verbose_name="Currency", default="TL")
    created_at = models.DateField(verbose_name="Created At", auto_now_add=True)
    updated_at = models.DateField(verbose_name="Last Updated At", auto_now=True)
    is_delete =  models.BooleanField(verbose_name="Is Active", default=False)

    def __str__(self):
        return f"{self.vehicle_cost} - {self.vehicle}  - {self.price} - {self.currency}" 
    
class Activitycost(models.Model):
    branch=models.ForeignKey(Branch, verbose_name="Branch", on_delete=models.CASCADE)
    supplier = models.ForeignKey(Activitysupplier, verbose_name="Activity Supplier", on_delete=models.SET_NULL, blank=True, null=True)
    activity = models.ForeignKey(Activity, verbose_name="Activity", on_delete=models.SET_NULL, blank=True, null=True)
    price = models.DecimalField(verbose_name="Price", max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, verbose_name="Currency", default="TL")
    created_at = models.DateField(verbose_name="Created At", auto_now_add=True)
    updated_at = models.DateField(verbose_name="Last Updated At", auto_now=True)
    is_delete =  models.BooleanField(verbose_name="Is Active", default=False)

    def __str__(self):
        return f"{self.supplier} - {self.activity}"
    
class Buyercompany(models.Model):
    branch=models.ForeignKey(Branch, verbose_name="Branch", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Name", max_length=100)
    short_name = models.CharField(verbose_name="Short Name", max_length=5, unique=True)
    contact = models.CharField(verbose_name="Contact", max_length=155, blank=True, null=True)
    created_at = models.DateField(verbose_name="Created At", auto_now_add=True)
    updated_at = models.DateField(verbose_name="Last Updated At", auto_now=True)
    is_delete =  models.BooleanField(verbose_name="Is Active", default=False)

    def __str__(self):
        return self.name
    
class UserActivityLog(models.Model):
    branch=models.ForeignKey(Branch, verbose_name="Branch", on_delete=models.CASCADE)
    staff = models.ForeignKey(Employee, verbose_name="Employee", on_delete=models.SET_NULL, blank=True, null=True)
    action = models.TextField()
    ip_address = models.GenericIPAddressField(verbose_name="IP Address", blank=True, null=True)
    browser_info = models.TextField(verbose_name="Tarayıcı Info", blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    created_at = models.DateField(verbose_name="Created At", auto_now_add=True)
    updated_at = models.DateField(verbose_name="Last Updated At", auto_now=True)
    is_delete =  models.BooleanField(verbose_name="Is Active", default=False)

    def __str__(self):
        return f"{self.staff} - {self.action} - {self.timestamp}"