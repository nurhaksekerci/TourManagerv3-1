from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import *

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'first_name', 'last_name', 'gender', 'phone', 'is_email_verified', 'is_phone_verified', 'is_active', 'two_factor_enabled')
    list_filter = ('is_email_verified', 'is_phone_verified', 'is_active', )
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone', 'profile_picture', 'is_email_verified', 'is_phone_verified', 'last_password_change', 'two_factor_enabled')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone', 'profile_picture', 'gender', 'is_email_verified', 'is_phone_verified', 'two_factor_enabled')}),
    )
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    ordering = ('email',)
    list_editable = ('is_email_verified', 'gender', 'is_phone_verified', 'is_active', 'two_factor_enabled')

admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_deleted', 'created_at', 'updated_at')
    list_editable = ('is_deleted',)
    search_fields = ('name',)

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'slug', 'is_deleted', 'created_at', 'updated_at')
    list_editable = ('is_deleted',)
    search_fields = ('name',)

@admin.register(Neighborhood)
class NeighborhoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'district', 'slug', 'is_deleted', 'created_at', 'updated_at')
    list_editable = ('is_deleted',)
    search_fields = ('name',)

@admin.register(SalesAgent)
class SalesAgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'neighborhood', 'district', 'city', 'number_of_sales', 'is_deleted', 'created_at', 'updated_at')
    list_editable = ('is_deleted',)
    search_fields = ('name',)

@admin.register(SalesAgentDoc)
class SalesAgentDocAdmin(admin.ModelAdmin):
    list_display = ('doc_name', 'sales_agent', 'is_deleted', 'created_at', 'updated_at')
    list_editable = ('is_deleted',)
    search_fields = ('doc_name',)

@admin.register(SalesAgentUser)
class SalesAgentUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'sales_agent', 'phone', 'is_manager', 'is_deleted', 'created_at', 'updated_at')
    list_editable = ('is_deleted',)
    search_fields = ('user__username',)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'district', 'neighborhood', 'is_deleted', 'created_at', 'updated_at')
    list_editable = ('is_deleted',)
    search_fields = ('name',)

@admin.register(SalesAgentCustomer)
class SalesAgentCustomerAdmin(admin.ModelAdmin):
    list_display = ('sales_agent', 'company', 'is_deleted', 'created_at', 'updated_at')
    list_editable = ('is_deleted',)
    search_fields = ('sales_agent__name',)

@admin.register(CompanyDoc)
class CompanyDocAdmin(admin.ModelAdmin):
    list_display = ('doc_name', 'company', 'is_deleted', 'created_at', 'updated_at')
    list_editable = ('is_deleted',)
    search_fields = ('doc_name',)

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'city', 'district', 'neighborhood', 'is_deleted', 'created_at', 'updated_at')
    list_editable = ('is_deleted',)
    search_fields = ('name',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'branch', 'is_manager', 'is_deleted', 'created_at', 'updated_at')
    list_editable = ('is_deleted',)
    search_fields = ('user__username',)
