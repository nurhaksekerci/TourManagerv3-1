from django.contrib import admin
from .models import (
    Vehicle, NoVehicleTour, Tour, Transfer, Hotel, Activity, Museum, Guide,
    VehicleSupplier, Activitysupplier, Vehiclecost, VehicleCostPrice,
    Activitycost, Buyercompany, UserActivityLog
)

class BaseAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'updated_at', 'is_delete']
    list_editable = ['is_delete']
    search_fields = ['branch__name']

@admin.register(Vehicle)
class VehicleAdmin(BaseAdmin):
    list_display = BaseAdmin.list_display + ['branch', 'vehicle', 'capacity']
    list_editable = BaseAdmin.list_editable + ['vehicle', 'capacity']

@admin.register(NoVehicleTour)
class NoVehicleTourAdmin(BaseAdmin):
    list_display = BaseAdmin.list_display + ['branch', 'route', 'city']
    list_editable = BaseAdmin.list_editable + ['route', 'city']

@admin.register(Tour)
class TourAdmin(BaseAdmin):
    list_display = BaseAdmin.list_display + ['branch', 'route', 'start_city', 'finish_city']
    list_editable = BaseAdmin.list_editable + ['route', 'start_city', 'finish_city']

@admin.register(Transfer)
class TransferAdmin(BaseAdmin):
    list_display = BaseAdmin.list_display + ['branch', 'route', 'start_city', 'finish_city']
    list_editable = BaseAdmin.list_editable + ['route', 'start_city', 'finish_city']

@admin.register(Hotel)
class HotelAdmin(BaseAdmin):
    list_display = BaseAdmin.list_display + ['branch', 'name', 'location', 'one_person', 'two_person', 'tree_person', 'currency']
    list_editable = BaseAdmin.list_editable + ['name', 'location', 'one_person', 'two_person', 'tree_person', 'currency']

@admin.register(Activity)
class ActivityAdmin(BaseAdmin):
    list_display = BaseAdmin.list_display + ['branch', 'name']
    list_editable = BaseAdmin.list_editable + ['name']

@admin.register(Museum)
class MuseumAdmin(BaseAdmin):
    list_display = BaseAdmin.list_display + ['branch', 'name', 'location', 'price', 'currency']
    list_editable = BaseAdmin.list_editable + ['name', 'location', 'price', 'currency']

@admin.register(Guide)
class GuideAdmin(BaseAdmin):
    list_display = BaseAdmin.list_display + ['branch', 'name', 'phone']
    list_editable = BaseAdmin.list_editable + ['name', 'phone']

@admin.register(VehicleSupplier)
class VehicleSupplierAdmin(BaseAdmin):
    list_display = BaseAdmin.list_display + ['branch', 'name']
    list_editable = BaseAdmin.list_editable + ['name']

@admin.register(Activitysupplier)
class ActivitySupplierAdmin(BaseAdmin):
    list_display = BaseAdmin.list_display + ['branch', 'name']
    list_editable = BaseAdmin.list_editable + ['name']

@admin.register(Vehiclecost)
class VehicleCostAdmin(BaseAdmin):
    list_display = BaseAdmin.list_display + ['branch', 'supplier', 'tour', 'transfer']
    list_editable = BaseAdmin.list_editable + ['supplier', 'tour', 'transfer']

@admin.register(VehicleCostPrice)
class VehicleCostPriceAdmin(BaseAdmin):
    list_display = BaseAdmin.list_display + ['vehicle_cost', 'vehicle', 'price', 'currency']
    list_editable = BaseAdmin.list_editable + ['vehicle_cost', 'vehicle', 'price', 'currency']

@admin.register(Activitycost)
class ActivityCostAdmin(BaseAdmin):
    list_display = BaseAdmin.list_display + ['branch', 'supplier', 'activity', 'price', 'currency']
    list_editable = BaseAdmin.list_editable + ['supplier', 'activity', 'price', 'currency']

@admin.register(Buyercompany)
class BuyercompanyAdmin(BaseAdmin):
    list_display = BaseAdmin.list_display + ['branch', 'name', 'short_name']
    list_editable = BaseAdmin.list_editable + ['name', 'short_name']

@admin.register(UserActivityLog)
class UserActivityLogAdmin(BaseAdmin):
    list_display = BaseAdmin.list_display + ['branch', 'staff', 'action', 'timestamp']
    list_editable = BaseAdmin.list_editable + ['staff', 'action']
