from django.contrib import admin
from .models import *

@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'client', 'start_at', 'finish_at', 'is_delete')
    list_editable = ('is_delete',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'operation', 'is_delete')
    list_editable = ('is_delete',)


@admin.register(SalesPrice)
class SalesPriceAdmin(admin.ModelAdmin):
    list_display = ('operation', 'price', 'currency', 'is_delete')
    list_editable = ('is_delete',)


@admin.register(OperationDay)
class OperationDayAdmin(admin.ModelAdmin):
    list_display = ('operation', 'date', 'is_delete')
    list_editable = ('is_delete',)

admin.site.register(OperationItem)
admin.site.register(OperationSubItem)