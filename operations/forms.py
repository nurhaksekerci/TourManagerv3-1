from decimal import Decimal
from django import forms
from .models import *
from datetime import date
from django.forms import TimeInput, inlineformset_factory
import datetime  # Bu satırı ekleyin

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
            'client': forms.Select(attrs={'class': 'form-control'}),
            'ticket': forms.TextInput(attrs={'class': 'form-control'}),
            'follow_employee': forms.Select(attrs={'class': 'form-control'}),
            'start_at': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'finish_at': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
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
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'passport': forms.TextInput(attrs={'class': 'form-control'}),
            'birthday': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'name': 'Name',
            'contact': 'Contact Information',
            'birthday': 'Date of Birth',
            'passport': 'Passport Number',
        }

    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')
        if birthday and birthday > date.today():
            raise forms.ValidationError("Doğum tarihi bugünden sonraki bir tarih olamaz.")
        return birthday
    
class SalesPriceForm(forms.ModelForm):
    class Meta:
        model = SalesPrice
        fields = [
            'price', 
            'currency'
        ]
        widgets = {
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),

        }
        labels = {
            'price': 'Price',
            'currency': 'Currency',
        }

CustomerFormSet = inlineformset_factory(
    Operation, Customer, form=CustomerForm, extra=1, can_delete=True
)

SalesPriceFormSet = inlineformset_factory(
    Operation, SalesPrice, form=SalesPriceForm, extra=1, can_delete=True
)


# Para birimi seçimleri
COST_CURRENCY_CHOICES = (
    ('USD', 'USD'),
    ('EUR', 'EUR'),
    ('TRY', 'TRY'),
)

SELL_CURRENCY_CHOICES = (
    ('USD', 'USD'),
    ('EUR', 'EUR'),
    ('TRY', 'TRY'),
    ('RMB', 'RMB'),
)

class DynamicOperationItemForm(forms.ModelForm):
    class Meta:
        model = OperationItem
        fields = ['order']

    def __init__(self, *args, **kwargs):
        item_type = kwargs.pop('item_type', None)
        self.item_no = kwargs.pop('item_no', None)
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['order'].required = False

        if request and request.user.is_authenticated:
            employee = Employee.objects.get(user=request.user)
            branch = employee.branch

            # item_type'ye göre dinamik alanları ekleyin
            if item_type == 'vehicle':
                self.fields['vehicle_type'] = forms.ModelChoiceField(
                    queryset=Vehicle.objects.filter(is_delete=False, branch=branch),
                    label="Araç Türü",
                    required=True
                )
                self.fields['driver_name'] = forms.CharField(label="Sürücü Adı", required=False)
                self.fields['driver_phone'] = forms.CharField(label="Sürücü Telefonu", required=False)
                self.fields['vehicle_plate'] = forms.CharField(label="Araç Plakası", required=False)
                self.fields['pickup_time'] = forms.TimeField(label="Alış Saati", required=True, widget=TimeInput(format='%H:%M', attrs={'type': 'time'}))
                self.fields['pickup_location'] = forms.CharField(label="Alış Yeri", required=True)
                self.fields['cost_price'] = forms.DecimalField(label="Maliyet Fiyatı", max_digits=10, decimal_places=2, required=False)
                self.fields['cost_currency'] = forms.ChoiceField(label="Maliyet Para Birimi", choices=COST_CURRENCY_CHOICES, required=False)
                self.add_fields()
            elif item_type == 'create_vehicle':
                self.fields['vehicle_type'] = forms.ModelChoiceField(
                    queryset=Vehicle.objects.filter(is_delete=False, branch=branch),
                    label="Araç Türü",
                    required=True
                )
                self.fields['pickup_time'] = forms.TimeField(label="Alış Saati", required=True, widget=TimeInput(format='%H:%M', attrs={'type': 'time'}))
                self.fields['pickup_location'] = forms.CharField(label="Alış Yeri", required=True)
                self.add_fields()
            elif item_type == 'walking_tour':
                self.fields['waling_tour'] = forms.ModelChoiceField(
                    queryset=NoVehicleTour.objects.filter(is_delete=False, branch=branch),
                    label="Yürüyüş Turu",
                    required=True
                )
                self.fields['pickup_time'] = forms.TimeField(label="Alış Saati", required=True, widget=TimeInput(format='%H:%M', attrs={'type': 'time'}))
                self.fields['pickup_location'] = forms.CharField(label="Alış Yeri", required=True)
                self.fields['sell_price'] = forms.DecimalField(label="Satış Fiyatı", max_digits=10, decimal_places=2, required=False)
                self.fields['sell_currency'] = forms.ChoiceField(label="Satış Para Birimi", choices=SELL_CURRENCY_CHOICES, required=False)
                self.fields['cost_price'] = forms.DecimalField(label="Maliyet Fiyatı", max_digits=10, decimal_places=2, required=False)
                self.fields['cost_currency'] = forms.ChoiceField(label="Maliyet Para Birimi", choices=COST_CURRENCY_CHOICES, required=False)
                self.add_fields()
            elif item_type == 'create_walking_tour':
                self.fields['waling_tour'] = forms.ModelChoiceField(
                    queryset=NoVehicleTour.objects.filter(is_delete=False, branch=branch),
                    label="Yürüyüş Turu",
                    required=True
                )
                self.fields['pickup_time'] = forms.TimeField(label="Alış Saati", required=True, widget=TimeInput(format='%H:%M', attrs={'type': 'time'}))
                self.fields['pickup_location'] = forms.CharField(label="Alış Yeri", required=True)
                self.fields['sell_price'] = forms.DecimalField(label="Satış Fiyatı", max_digits=10, decimal_places=2, required=False)
                self.fields['sell_currency'] = forms.ChoiceField(label="Satış Para Birimi", choices=SELL_CURRENCY_CHOICES, required=False)
                self.add_fields()
            elif item_type == 'walking_activity':
                self.fields['pickup_time'] = forms.TimeField(label="Alış Saati", required=True, widget=TimeInput(format='%H:%M', attrs={'type': 'time'}))
                self.fields['pickup_location'] = forms.CharField(label="Alış Yeri", required=True)
                self.fields['sell_price'] = forms.DecimalField(label="Satış Fiyatı", max_digits=10, decimal_places=2, required=False)
                self.fields['sell_currency'] = forms.ChoiceField(label="Satış Para Birimi", choices=SELL_CURRENCY_CHOICES, required=False)
                self.fields['cost_price'] = forms.DecimalField(label="Maliyet Fiyatı", max_digits=10, decimal_places=2, required=False)
                self.fields['cost_currency'] = forms.ChoiceField(label="Maliyet Para Birimi", choices=COST_CURRENCY_CHOICES, required=False)
                self.add_fields()
            elif item_type == 'create_walking_activity':
                self.fields['pickup_time'] = forms.TimeField(label="Alış Saati", required=True, widget=TimeInput(format='%H:%M', attrs={'type': 'time'}))
                self.fields['pickup_location'] = forms.CharField(label="Alış Yeri", required=True)
                self.fields['sell_price'] = forms.DecimalField(label="Satış Fiyatı", max_digits=10, decimal_places=2, required=False)
                self.fields['sell_currency'] = forms.ChoiceField(label="Satış Para Birimi", choices=SELL_CURRENCY_CHOICES, required=False)
                self.add_fields()
            
            # Zorunlu alanlara * ekleyin
            for field_name, field in self.fields.items():
                if field.required:
                    field.label += " *"

    def add_fields(self):
        # Benzersiz `item_no` değerini ekleyin
        self.fields['item_no'] = forms.CharField(label="item no", required=False, initial=self.item_no)

    def clean(self):
        cleaned_data = super().clean()
        
        # JSON serileştirilebilir `attributes` oluşturmak için gerekli dönüşümler
        dynamic_attributes = {
            field: (
                cleaned_data[field].strftime('%H:%M') if isinstance(cleaned_data[field], datetime.time) else
                cleaned_data[field].id if isinstance(cleaned_data[field], (Vehicle, NoVehicleTour)) else
                str(cleaned_data[field]) if isinstance(cleaned_data[field], Decimal) else
                cleaned_data[field]
            )
            for field in self.fields
            if field not in ['order', 'item_no', 'operation_day']
        }
        
        print("Dynamic Attributes before saving:", dynamic_attributes)  # Debug için
        
        cleaned_data['attributes'] = dynamic_attributes if dynamic_attributes else None
        return cleaned_data




    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # `attributes`'u `cleaned_data`'den al ve debug için çıktı al
        instance.attributes = self.cleaned_data.get('attributes')
        print("Instance attributes before saving:", instance.attributes)  # Debug için
        
        if commit:
            instance.save()
        return instance



class DynamicOperationSubItemForm(forms.ModelForm):
    class Meta:
        model = OperationSubItem
        fields = ['order']

    def __init__(self, *args, sub_item_type=None, sub_item_no=None, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        if request and request.user.is_authenticated:
            employee = Employee.objects.get(user=request.user)
            branch = employee.branch

            # `sub_item_type`'a göre dinamik alanları ekliyoruz
            if sub_item_type == 'tour':
                self.fields['tour'] = forms.ModelChoiceField(
                    queryset=Tour.objects.filter(is_delete=False, branch=branch),
                    label="Tur Yeri",
                    required=True
                )
                self.add_price_fields()
                self.create_add_price_fields(sub_item_no)
            
            if sub_item_type == 'create_tour':
                self.fields['tour'] = forms.ModelChoiceField(
                    queryset=Tour.objects.filter(is_delete=False, branch=branch),
                    label="Tur Yeri",
                    required=True
                )
                self.create_add_price_fields(sub_item_no)

            elif sub_item_type == 'transfer':
                self.fields['transfer'] = forms.ModelChoiceField(
                    queryset=Transfer.objects.filter(is_delete=False, branch=branch),
                    label="Transfer Yeri",
                    required=True
                )
                self.add_price_fields()
                self.create_add_price_fields(sub_item_no)

            elif sub_item_type == 'create_transfer':
                self.fields['transfer'] = forms.ModelChoiceField(
                    queryset=Transfer.objects.filter(is_delete=False, branch=branch),
                    label="Transfer Yeri",
                    required=True
                )
                self.create_add_price_fields(sub_item_no)

            elif sub_item_type == 'hotel':
                self.fields['hotel'] = forms.ModelChoiceField(
                    queryset=Hotel.objects.filter(is_delete=False, branch=branch),
                    label="Otel Adı",
                    required=True
                )
                self.fields['room_type'] = forms.CharField(label="Oda Tipi", required=False)
                self.add_price_fields()
                self.create_add_price_fields(sub_item_no)

            elif sub_item_type == 'create_hotel':
                self.fields['hotel'] = forms.ModelChoiceField(
                    queryset=Hotel.objects.filter(is_delete=False, branch=branch),
                    label="Otel Adı",
                    required=True
                )
                self.fields['room_type'] = forms.CharField(label="Oda Tipi", required=False)
                self.create_add_price_fields(sub_item_no)

            elif sub_item_type == 'activity':
                self.fields['activity_name'] = forms.ModelChoiceField(
                    queryset=Activity.objects.filter(is_delete=False, branch=branch),
                    label="Aktivite Adı",
                    required=True
                )
                self.add_price_fields()
                self.create_add_price_fields(sub_item_no)

            elif sub_item_type == 'create_activity':
                self.fields['activity_name'] = forms.ModelChoiceField(
                    queryset=Activity.objects.filter(is_delete=False, branch=branch),
                    label="Aktivite Adı",
                    required=True
                )
                self.create_add_price_fields(sub_item_no)

            elif sub_item_type == 'museum':
                self.fields['museums'] = forms.ModelMultipleChoiceField(
                    queryset=Museum.objects.filter(is_delete=False, branch=branch),
                    label="Müzeler",
                    required=True,
                    widget=forms.CheckboxSelectMultiple
                )
                self.add_price_fields()
                self.create_add_price_fields(sub_item_no)

            elif sub_item_type == 'create_museum':
                self.fields['museums'] = forms.ModelMultipleChoiceField(
                    queryset=Museum.objects.filter(is_delete=False, branch=branch),
                    label="Müzeler",
                    required=True,
                    widget=forms.CheckboxSelectMultiple
                )
                self.create_add_price_fields(sub_item_no)

            elif sub_item_type == 'guide':
                self.fields['guide'] = forms.ModelChoiceField(
                    queryset=Guide.objects.filter(is_delete=False, branch=branch),
                    label="Rehber Adı",
                    required=True
                )
                self.add_price_fields()
                self.create_add_price_fields(sub_item_no)

            elif sub_item_type == 'create_guide':
                self.fields['guide'] = forms.ModelChoiceField(
                    queryset=Guide.objects.filter(is_delete=False, branch=branch),
                    label="Rehber Adı",
                    required=True
                )
                self.create_add_price_fields(sub_item_no)

            elif sub_item_type == 'other_price':
                self.fields['name'] = forms.CharField(label="Adı", required=False)
                self.fields['other_price'] = forms.DecimalField(label="Diğer Fiyat", max_digits=10, decimal_places=2, required=False)
                self.fields['other_currency'] = forms.ChoiceField(label="Diğer Para Birimi", choices=SELL_CURRENCY_CHOICES, required=False)
                self.add_price_fields()
                self.create_add_price_fields(sub_item_no)

            elif sub_item_type == 'create_other_price':
                self.fields['name'] = forms.CharField(label="Adı", required=False)
                self.fields['other_price'] = forms.DecimalField(label="Diğer Fiyat", max_digits=10, decimal_places=2, required=False)
                self.fields['other_currency'] = forms.ChoiceField(label="Diğer Para Birimi", choices=SELL_CURRENCY_CHOICES, required=False)
                self.create_add_price_fields(sub_item_no)

            # Zorunlu alanların etiketine "*" ekliyoruz
            for field_name, field in self.fields.items():
                if field.required:
                    field.label += " *"

    def add_price_fields(self):
        self.fields['cost_price'] = forms.DecimalField(label="Maliyet Fiyatı", max_digits=10, decimal_places=2, required=False)
        self.fields['cost_currency'] = forms.ChoiceField(label="Maliyet Para Birimi", choices=COST_CURRENCY_CHOICES, required=False)


    def create_add_price_fields(self, sub_item_no):
        self.fields['sell_price'] = forms.DecimalField(label="Satış Fiyatı", max_digits=10, decimal_places=2, required=False)
        self.fields['sell_currency'] = forms.ChoiceField(label="Satış Para Birimi", choices=SELL_CURRENCY_CHOICES, required=False)
        self.fields['mini_desc'] = forms.CharField(label="Açıklama", required=False)
        self.fields['sub_item_no'] = forms.CharField(label="item no", required=False, initial=sub_item_no)

    def clean(self):
        cleaned_data = super().clean()
        # `attributes` alanına `order` dışındaki alanları JSON olarak ekliyoruz
        attributes = {field: cleaned_data[field] for field in self.fields if field not in ['order']}
        cleaned_data['attributes'] = attributes
        return cleaned_data
    
