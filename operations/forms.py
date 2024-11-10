from django import forms
from .models import *

class OperationForm(forms.ModelForm):
    class Meta:
        model = Operation
        fields = [
            'client', 
            'ticket', 
            'follow_employee', 
            'start_at', 
            'finish_at', 
        ]
        widgets = {
            'start_at': forms.DateInput(attrs={'type': 'date'}),
            'finish_at': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'client': 'Buyer Company',
            'ticket': 'Ticket',
            'follow_employee': 'Employee who follows up',
            'start_at': 'Start Date',
            'finish_at': 'Finish Date',
        }

    def clean_finish_at(self):
        start_at = self.cleaned_data.get('start_at')
        finish_at = self.cleaned_data.get('finish_at')
        if finish_at and start_at and finish_at < start_at:
            raise forms.ValidationError("Finish date cannot be earlier than start date.")
        return finish_at


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'name', 
            'contact', 
            'birthday', 
            'passport'
        ]
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'name': 'Name',
            'contact': 'Contact Information',
            'birthday': 'Date of Birth',
            'passport': 'Passport Number',
        }

    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')
        if birthday and birthday > forms.fields.date.today():
            raise forms.ValidationError("Birthday cannot be a future date.")
        return birthday
    
class SalesPriceForm(forms.ModelForm):
    class Meta:
        model = SalesPrice
        fields = [
            'price', 
            'currency'
        ]
        labels = {
            'price': 'Price',
            'currency': 'Currency',
        }

class OperationItemVehicleForm(forms.ModelForm):
    class Meta:
        model = OperationItemVehicle
        fields = [
            'vehicle',  
            'sell_price', 
            'sell_currency'
        ]
        labels = {
            'vehicle': 'Vehicle',
            'sell_price': 'Sell Price',
            'sell_currency': 'Sell Currency',
        }

class OperationItemVehicleUpdateForm(forms.ModelForm):
    class Meta:
        model = OperationItemVehicle
        fields = [
            'vehicle', 
            'vehicle_supplier', 
            'driver_name', 
            'driver_phone', 
            'vehicle_plate', 
            'vehicle_cost', 
            'cost_price', 
            'cost_currency', 
            'sell_price', 
            'sell_currency'
        ]
        labels = {
            'vehicle': 'Vehicle',
            'vehicle_supplier': 'Vehicle Supplier',
            'driver_name': 'Driver Name',
            'driver_phone': 'Driver Phone',
            'vehicle_plate': 'Vehicle Plate',
            'vehicle_cost': 'Vehicle Cost',
            'cost_price': 'Cost Price',
            'cost_currency': 'Cost Currency',
            'sell_price': 'Sell Price',
            'sell_currency': 'Sell Currency',
        }
        widgets = {
            'driver_phone': forms.TextInput(attrs={'placeholder': 'e.g., 5554443322'}),
        }

class OperationItemNoVehicleTourForm(forms.ModelForm):
    class Meta:
        model = OperationItemNoVehicleTour
        fields = [
            'novehicletour',  
            'sell_price', 
            'sell_currency'
        ]
        labels = {
            'novehicletour': 'No Vehicle Tour',
            'sell_price': 'Sell Price',
            'sell_currency': 'Sell Currency',
        }

class OperationItemNoVehicleTourUpdateForm(forms.ModelForm):
    class Meta:
        model = OperationItemNoVehicleTour
        fields = [
            'novehicletour', 
            'cost_price', 
            'cost_currency', 
            'sell_price', 
            'sell_currency'
        ]
        labels = {
            'novehicletour': 'No Vehicle Tour',
            'cost_price': 'Cost Price',
            'cost_currency': 'Cost Currency',
            'sell_price': 'Sell Price',
            'sell_currency': 'Sell Currency',
        }


class OperationItemNoVehicleActivityForm(forms.ModelForm):
    class Meta:
        model = OperationItemNoVehicleActivity
        fields = [
            'activity', 
            'sell_price', 
            'sell_currency'
        ]
        labels = {
            'activity': 'Activity',
            'sell_price': 'Sell Price',
            'sell_currency': 'Sell Currency',
        }

class OperationItemNoVehicleActivityUpdateForm(forms.ModelForm):
    class Meta:
        model = OperationItemNoVehicleActivity
        fields = [
            'activity', 
            'activity_supplier', 
            'cost_price', 
            'cost_currency', 
            'sell_price', 
            'sell_currency'
        ]
        labels = {
            'activity': 'Activity',
            'activity_supplier': 'Activity Supplier',
            'cost_price': 'Cost Price',
            'cost_currency': 'Cost Currency',
            'sell_price': 'Sell Price',
            'sell_currency': 'Sell Currency',
        }


class OperationItemTourForm(forms.ModelForm):
    class Meta:
        model = OperationItemTour
        fields = [
            'tour', 
            'sell_price', 
            'sell_currency',
            'mini_description'
        ]
        labels = {
            'tour': 'Tour',
            'sell_price': 'Sell Price',
            'sell_currency': 'Sell Currency',
            'mini_description': 'Mini Description',
        }

class OperationItemTourUpdateForm(forms.ModelForm):
    class Meta:
        model = OperationItemTour
        fields = [
            'tour',
            'cost_price', 
            'cost_currency', 
            'sell_price', 
            'sell_currency',
            'mini_description'
        ]
        labels = {
            'tour': 'Tour',
            'cost_price': 'Cost Price',
            'cost_currency': 'Cost Currency',
            'sell_price': 'Sell Price',
            'sell_currency': 'Sell Currency',
            'mini_description': 'Mini Description',
        }

class OperationItemTransferForm(forms.ModelForm):
    class Meta:
        model = OperationItemTransfer
        fields = [
            'transfer', 
            'sell_price', 
            'sell_currency',
            'mini_description'
        ]
        labels = {
            'transfer': 'Transfer',
            'sell_price': 'Sell Price',
            'sell_currency': 'Sell Currency',
            'mini_description': 'Mini Description',
        }

class OperationItemTransferUpdateForm(forms.ModelForm):
    class Meta:
        model = OperationItemTransfer
        fields = [
            'transfer',
            'cost_price', 
            'cost_currency', 
            'sell_price', 
            'sell_currency',
            'mini_description'
        ]
        labels = {
            'transfer': 'Transfer',
            'cost_price': 'Cost Price',
            'cost_currency': 'Cost Currency',
            'sell_price': 'Sell Price',
            'sell_currency': 'Sell Currency',
            'mini_description': 'Mini Description',
        }