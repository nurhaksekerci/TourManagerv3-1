from django.db import models
from company.models import *
from files.models import *

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
    company = models.ForeignKey(Company, verbose_name="Company", related_name="operations", on_delete=models.CASCADE)
    client = models.ForeignKey(Buyercompany, verbose_name=("Buyer Company"), on_delete=models.CASCADE)
    ticket = models.CharField(verbose_name="Ticket", max_length=255)
    follow_employee = models.ForeignKey(Employee, verbose_name="Employee who follows up", related_name="follows", on_delete=models.CASCADE)
    create_employee = models.ForeignKey(Employee, verbose_name="Employee who creates", related_name="creates", on_delete=models.CASCADE)
    start_at = models.DateField(verbose_name="Start At")
    finish_at = models.DateField(verbose_name="Finish At")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_delete =  models.BooleanField(verbose_name="Is Active", default=False)

    def __str__(self):
        return f"Operation {self.ticket} ({self.start_at} - {self.finish_at})"


class Customer(models.Model):
    company = models.ForeignKey(Company, verbose_name="Company", related_name="customers", on_delete=models.CASCADE)
    operation = models.ForeignKey(Operation, verbose_name="Operation", related_name="customers", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Name", max_length=255)
    contact = models.CharField(verbose_name="Contact", max_length=255, blank=True, null=True)
    birthday = models.DateField(verbose_name="Birthday", default="1900-01-01")
    passport = models.CharField(verbose_name="Passport", max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_delete =  models.BooleanField(verbose_name="Is Active", default=False)

    def __str__(self):
        return f"{self.name} ({self.passport})"


class SalesPrice(models.Model):
    company = models.ForeignKey(Company, verbose_name="Company", related_name="sales_prices", on_delete=models.CASCADE)
    operation = models.ForeignKey(Operation, verbose_name="Operation", related_name="sales_prices", on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name="Price", max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=SELLCURRENCY_CHOICES, default='USD')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_delete =  models.BooleanField(verbose_name="Is Active", default=False)

    def __str__(self):
        return f"{self.operation.ticket} - {self.price} {self.currency}"


class OperationDay(models.Model):
    company = models.ForeignKey(Company, verbose_name="Company", related_name="operation_days", on_delete=models.CASCADE)
    operation = models.ForeignKey(Operation, verbose_name="Operation", related_name="operation_days", on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Date")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_delete =  models.BooleanField(verbose_name="Is Active", default=False)

    def __str__(self):
        return f"{self.operation.ticket} - {self.date}"


class OperationItemVehicle(models.Model):
    company = models.ForeignKey(Company, verbose_name="Company", related_name="operation_items_company", on_delete=models.CASCADE)
    operation = models.ForeignKey(Operation, verbose_name="Operation", related_name="operation_items_operation", on_delete=models.CASCADE)
    day = models.ForeignKey(OperationDay, verbose_name="Operation Days", related_name="operation_items_day", on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, verbose_name=("Vehicle"), on_delete=models.CASCADE, related_name="operation_items_day")
    vehicle_supplier = models.ForeignKey(VehicleSupplier, verbose_name="Vehicle Supplier", related_name="tour_suppliers", on_delete=models.CASCADE, blank=True, null=True)
    driver_name = models.CharField(verbose_name="Driver Name", max_length=255, blank=True, null=True)
    driver_phone = models.CharField(verbose_name="Driver Phone", max_length=255, blank=True, null=True)
    vehicle_plate = models.CharField(verbose_name="Vehicle Plate", max_length=255, blank=True, null=True)
    vehicle_cost = models.ForeignKey(Vehiclecost, verbose_name="Vehicle Cost", related_name="tour_vehicle_costs", on_delete=models.CASCADE, blank=True, null=True)
    cost_price = models.DecimalField(verbose_name="Cost Price", max_digits=10, decimal_places=2, blank=True, null=True)
    cost_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    sell_price = models.DecimalField(verbose_name="Sell Price", max_digits=10, decimal_places=2, blank=True, null=True)
    sell_currency = models.CharField(max_length=3, choices=SELLCURRENCY_CHOICES, default='USD')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_delete =  models.BooleanField(verbose_name="Is Active", default=False)

    def __str__(self):
        return f"{self.operation.ticket} - on {self.day.date}"

class OperationItemNoVehicleTour(models.Model):
    company = models.ForeignKey(Company, verbose_name="Company", related_name="operation_items_company", on_delete=models.CASCADE)
    operation = models.ForeignKey(Operation, verbose_name="Operation", related_name="operation_items_operation", on_delete=models.CASCADE)
    day = models.ForeignKey(OperationDay, verbose_name="Operation Days", related_name="operation_items_day", on_delete=models.CASCADE)
    novehicletour = models.ForeignKey(NoVehicleTour, verbose_name=("No Vehicle Tour"), on_delete=models.CASCADE, related_name="operation_items_day")
    cost_price = models.DecimalField(verbose_name="Cost Price", max_digits=10, decimal_places=2, blank=True, null=True)
    cost_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    sell_price = models.DecimalField(verbose_name="Sell Price", max_digits=10, decimal_places=2, blank=True, null=True)
    sell_currency = models.CharField(max_length=3, choices=SELLCURRENCY_CHOICES, default='USD')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_delete =  models.BooleanField(verbose_name="Is Active", default=False)

    def __str__(self):
        return f"{self.operation.ticket} - on {self.day.date}"

class OperationItemNoVehicleActivity(models.Model):
    company = models.ForeignKey(Company, verbose_name="Company", related_name="operation_items_company", on_delete=models.CASCADE)
    operation = models.ForeignKey(Operation, verbose_name="Operation", related_name="operation_items_operation", on_delete=models.CASCADE)
    day = models.ForeignKey(OperationDay, verbose_name="Operation Days", related_name="operation_items_day", on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, verbose_name=("Activity"), on_delete=models.CASCADE, related_name="operation_items_activity")
    activity_supplier = models.ForeignKey(Activitysupplier, verbose_name=("Activity Supplier"), related_name="operation_items_activity_supplier", on_delete=models.CASCADE)
    cost_price = models.DecimalField(verbose_name="Cost Price", max_digits=10, decimal_places=2, blank=True, null=True)
    cost_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    sell_price = models.DecimalField(verbose_name="Sell Price", max_digits=10, decimal_places=2, blank=True, null=True)
    sell_currency = models.CharField(max_length=3, choices=SELLCURRENCY_CHOICES, default='USD')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_delete =  models.BooleanField(verbose_name="Is Active", default=False)

    def __str__(self):
        return f"{self.operation.ticket} - on {self.day.date}"


class OperationItemTour(models.Model):
    company = models.ForeignKey(Company, verbose_name="Company", related_name="operation_item_tours", on_delete=models.CASCADE)
    operation_item_vehicle = models.ForeignKey(OperationItemVehicle, verbose_name="Operation Item Vehicle", related_name="tour_details", on_delete=models.CASCADE)
    serial_number = models.PositiveIntegerField(verbose_name=("Serial Number"), blank=True, null=True)
    tour = models.ForeignKey(Tour, verbose_name="Tour", related_name="operation_tours", on_delete=models.CASCADE)
    cost_price = models.DecimalField(verbose_name="Cost Price", max_digits=10, decimal_places=2, blank=True, null=True)
    cost_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    sell_price = models.DecimalField(verbose_name="Sell Price", max_digits=10, decimal_places=2, blank=True, null=True)
    sell_currency = models.CharField(max_length=3, choices=SELLCURRENCY_CHOICES, default='USD')
    mini_description = models.CharField(verbose_name=("Mini Description"), max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_delete =  models.BooleanField(verbose_name="Is Active", default=False)

    def __str__(self):
        return f"{self.operation_item_vehicle.operation.ticket} - Tour {self.tour.route}"


class OperationItemTransfer(models.Model):
    company = models.ForeignKey(Company, verbose_name="Company", related_name="operation_item_transfers", on_delete=models.CASCADE)
    operation_item_vehicle = models.ForeignKey(OperationItemVehicle, verbose_name="Operation Item Vehicle", related_name="transfer_details", on_delete=models.CASCADE)
    serial_number = models.PositiveIntegerField(verbose_name=("Serial Number"), blank=True, null=True)
    transfer = models.ForeignKey(Transfer, verbose_name="Transfer", related_name="operation_transfers", on_delete=models.CASCADE)
    cost_price = models.DecimalField(verbose_name="Cost Price", max_digits=10, decimal_places=2, blank=True, null=True)
    cost_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    sell_price = models.DecimalField(verbose_name="Sell Price", max_digits=10, decimal_places=2, blank=True, null=True)
    sell_currency = models.CharField(max_length=3, choices=SELLCURRENCY_CHOICES, default='USD')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_delete =  models.BooleanField(verbose_name="Is Active", default=False)

    def __str__(self):
        return f"{self.operation_item_vehicle.operation.ticket} - Transfer {self.transfer.route}"
    
class OperationItemHotel(models.Model):
    company = models.ForeignKey(Company, verbose_name="Company", related_name="operation_item_hotels", on_delete=models.CASCADE)
    operation_item_vehicle = models.ForeignKey(OperationItemVehicle, verbose_name="Operation Item Vehicle", related_name="hotel_details", on_delete=models.CASCADE)
    serial_number = models.PositiveIntegerField(verbose_name=("Serial Number"), blank=True, null=True)
    hotel = models.ForeignKey(Hotel, verbose_name="Hotel", related_name="operation_hotels", on_delete=models.CASCADE)
    hotel_sell_price = models.DecimalField(verbose_name="Sell Price", max_digits=10, decimal_places=2, blank=True, null=True)
    hotel_sell_currency = models.CharField(max_length=3, choices=SELLCURRENCY_CHOICES, default='USD')
    hotel_cost_price = models.DecimalField(verbose_name="Cost Price", max_digits=10, decimal_places=2, blank=True, null=True)
    hotel_cost_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    we_paid = models.BooleanField(verbose_name="We Paid", default=False)
    mini_description = models.CharField(verbose_name=("Mini Description"), max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_delete =  models.BooleanField(verbose_name="Is Active", default=False)

    def __str__(self):
        return f"{self.operation_item_vehicle.operation.ticket} - Hotel {self.hotel.name}"


class OperationItemActivity(models.Model):
    company = models.ForeignKey(Company, verbose_name="Company", related_name="operation_item_activities", on_delete=models.CASCADE)
    operation_item_vehicle = models.ForeignKey(OperationItemVehicle, verbose_name="Operation Item Vehicle", related_name="activity_details", on_delete=models.CASCADE)
    operation_item_novehicle_tour = models.ForeignKey(OperationItemNoVehicleTour, verbose_name="Operation Item Vehicle", related_name="activity_details", on_delete=models.CASCADE)
    serial_number = models.PositiveIntegerField(verbose_name=("Serial Number"), blank=True, null=True)
    activity = models.ForeignKey(Activity, verbose_name="Activity", related_name="operation_activities", on_delete=models.CASCADE)
    activity_supplier = models.ForeignKey(Activitysupplier, verbose_name="Activity Supplier", related_name="operation_activity_suppliers", on_delete=models.CASCADE, blank=True, null=True)
    activity_sell_price = models.DecimalField(verbose_name="Sell Price", max_digits=10, decimal_places=2, blank=True, null=True)
    activity_sell_currency = models.CharField(max_length=3, choices=SELLCURRENCY_CHOICES, default='USD')
    activity_cost_price = models.DecimalField(verbose_name="Cost Price", max_digits=10, decimal_places=2, blank=True, null=True)
    activity_cost_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    we_paid = models.BooleanField(verbose_name="We Paid", default=False)
    mini_description = models.CharField(verbose_name=("Mini Description"), max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_delete =  models.BooleanField(verbose_name="Is Active", default=False)

    def __str__(self):
        return f"{self.operation_item_vehicle.operation.ticket} - Activity {self.activity.name}"


class OperationItemMuseum(models.Model):
    company = models.ForeignKey(Company, verbose_name="Company", related_name="operation_item_museums", on_delete=models.CASCADE)
    operation_item_vehicle = models.ForeignKey(OperationItemVehicle, verbose_name="Operation Item Vehicle", related_name="museum_details", on_delete=models.CASCADE)
    operation_item_novehicle_tour = models.ForeignKey(OperationItemNoVehicleTour, verbose_name="Operation Item Vehicle", related_name="museum_details", on_delete=models.CASCADE)
    operation_item_novehicle_activity = models.ForeignKey(OperationItemNoVehicleActivity, verbose_name="Operation Item Vehicle", related_name="museum_details", on_delete=models.CASCADE)
    serial_number = models.PositiveIntegerField(verbose_name=("Serial Number"), blank=True, null=True)
    museums = models.ManyToManyField(Museum, verbose_name="Museums")
    museum_sell_price = models.DecimalField(verbose_name="Sell Price", max_digits=10, decimal_places=2, blank=True, null=True)
    museum_sell_currency = models.CharField(max_length=3, choices=SELLCURRENCY_CHOICES, default='USD')
    museum_cost_price = models.DecimalField(verbose_name="Cost Price", max_digits=10, decimal_places=2, blank=True, null=True)
    museum_cost_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    we_paid = models.BooleanField(verbose_name="We Paid", default=False)
    mini_description = models.CharField(verbose_name=("Mini Description"), max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_delete =  models.BooleanField(verbose_name="Is Active", default=False)

    def __str__(self):
        museum_names = ', '.join([museum.name for museum in self.museums.all()])
        return f"{self.operation_item_vehicle.operation.ticket} - Museums: {museum_names}"


class OperationItemGuide(models.Model):
    company = models.ForeignKey(Company, verbose_name="Company", related_name="operation_item_guides", on_delete=models.CASCADE)
    operation_item_vehicle = models.ForeignKey(OperationItemVehicle, verbose_name="Operation Item Vehicle", related_name="guide_details", on_delete=models.CASCADE, blank=True, null=True)
    operation_item_novehicle_tour = models.ForeignKey(OperationItemNoVehicleTour, verbose_name="Operation Item Vehicle", related_name="guide_details", on_delete=models.CASCADE, blank=True, null=True)
    operation_item_novehicle_activity = models.ForeignKey(OperationItemNoVehicleActivity, verbose_name="Operation Item Vehicle", related_name="guide_details", on_delete=models.CASCADE, blank=True, null=True)
    is_there = models.BooleanField(verbose_name="Is There", default=True)
    guide = models.ForeignKey(Guide, verbose_name="Guide", related_name="operation_guides", on_delete=models.CASCADE, blank=True, null=True)
    guide_cost_price = models.DecimalField(verbose_name="Cost Price", max_digits=10, decimal_places=2, blank=True, null=True)
    guide_cost_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    guide_sell_price = models.DecimalField(verbose_name="Sell Price", max_digits=10, decimal_places=2, blank=True, null=True)
    guide_sell_currency = models.CharField(max_length=3, choices=SELLCURRENCY_CHOICES, default='USD')
    mini_description = models.CharField(verbose_name=("Mini Description"), max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_delete =  models.BooleanField(verbose_name="Is Active", default=False)

    def __str__(self):
        return f"{self.operation_item_vehicle.operation.ticket}"



class OperationItemOtherPrice(models.Model):
    company = models.ForeignKey(Company, verbose_name="Company", related_name="operation_item_other_prices", on_delete=models.CASCADE)
    operation_item_vehicle = models.ForeignKey(OperationItemVehicle, verbose_name="Operation Item Vehicle", related_name="other_price_details", on_delete=models.CASCADE)
    operation_item_novehicle_tour = models.ForeignKey(OperationItemNoVehicleTour, verbose_name="Operation Item Vehicle", related_name="other_price_details", on_delete=models.CASCADE)
    operation_item_novehicle_activity = models.ForeignKey(OperationItemNoVehicleActivity, verbose_name="Operation Item Vehicle", related_name="other_price_details", on_delete=models.CASCADE)
    serial_number = models.PositiveIntegerField(verbose_name=("Serial Number"), blank=True, null=True)
    other_name = models.CharField(verbose_name="Other Name", max_length=255, blank=True, null=True)
    other_cost_price = models.DecimalField(verbose_name="Cost Price", max_digits=10, decimal_places=2, blank=True, null=True)
    other_cost_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    other_sell_price = models.DecimalField(verbose_name="Sell Price", max_digits=10, decimal_places=2, blank=True, null=True)
    other_sell_currency = models.CharField(max_length=3, choices=SELLCURRENCY_CHOICES, default='USD')
    mini_description = models.CharField(verbose_name=("Mini Description"), max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_delete =  models.BooleanField(verbose_name="Is Active", default=False)

    def __str__(self):
        return f"{self.operation_item_vehicle.operation.ticket} - Other Price {self.other_name}"

