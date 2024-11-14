from django import forms
from .models import *

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle', 'capacity']  # 'company' kaldırıldı
        widgets = {
            'vehicle': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'vehicle': "Araçlar",
            'capacity': "Kapasite",
        }
        help_texts = {
            'vehicle': 'Araç ismini giriniz.',
            'capacity': 'Araç kapasitesini belirtiniz.',
        }

    def clean_capacity(self):
        capacity = self.cleaned_data.get('capacity')
        if capacity <= 0:
            raise forms.ValidationError("Kapasite sıfırdan büyük olmalıdır.")
        return capacity

class NoVehicleTourForm(forms.ModelForm):
    class Meta:
        model = NoVehicleTour
        fields = ['route', 'city']  # 'company' ve 'is_delete' kaldırıldı
        widgets = {
            'route': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'route': "Güzergah",
            'city': "Başlangıç Şehri",
        }
        help_texts = {
            'route': 'Güzergah ismini giriniz.',
            'city': 'Başlangıç şehrini seçiniz.',
        }

    def clean_route(self):
        route = self.cleaned_data.get('route')
        if not route:
            raise forms.ValidationError("Güzergah boş olamaz.")
        return route
    
class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ['route', 'start_city', 'finish_city']  # 'company' ve 'is_delete' kaldırıldı
        widgets = {
            'route': forms.TextInput(attrs={'class': 'form-control'}),
            'start_city': forms.Select(attrs={'class': 'form-control'}),
            'finish_city': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'route': "Güzergah",
            'start_city': "Başlangıç Şehri",
            'finish_city': "Varış Şehri",
        }
        help_texts = {
            'route': 'Güzergah ismini giriniz.',
            'start_city': 'Başlangıç şehrini seçiniz.',
            'finish_city': 'Varış şehrini seçiniz.',
        }

    def clean_route(self):
        route = self.cleaned_data.get('route')
        if not route:
            raise forms.ValidationError("Güzergah boş olamaz.")
        return route
    
class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ['route', 'start_city', 'finish_city']  # 'company' ve 'is_delete' kaldırıldı
        widgets = {
            'route': forms.TextInput(attrs={'class': 'form-control'}),
            'start_city': forms.Select(attrs={'class': 'form-control'}),
            'finish_city': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'route': "Güzergah",
            'start_city': "Başlangıç Şehri",
            'finish_city': "Varış Şehri",
        }
        help_texts = {
            'route': 'Güzergah ismini giriniz.',
            'start_city': 'Başlangıç şehrini seçiniz.',
            'finish_city': 'Varış şehrini seçiniz.',
        }

    def clean_route(self):
        route = self.cleaned_data.get('route')
        if not route:
            raise forms.ValidationError("Güzergah boş olamaz.")
        return route
    

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'location', 'mail', 'one_person', 'two_person', 'tree_person', 'finish', 'currency']  # 'company' ve 'is_delete' kaldırıldı
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
            'mail': forms.EmailInput(attrs={'class': 'form-control'}),
            'one_person': forms.NumberInput(attrs={'class': 'form-control'}),
            'two_person': forms.NumberInput(attrs={'class': 'form-control'}),
            'tree_person': forms.NumberInput(attrs={'class': 'form-control'}),
            'finish': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': "Otel Adı",
            'location': "Konum",
            'mail': "E-posta",
            'one_person': "Tek Kişilik Ücret",
            'two_person': "İki Kişilik Ücret",
            'tree_person': "Üç Kişilik Ücret",
            'finish': "Fiyat Geçerlilik Tarihi",
            'currency': "Para Birimi",
        }
        help_texts = {
            'name': 'Otelin adını giriniz.',
            'location': 'Otelin bulunduğu şehri seçiniz.',
            'mail': 'Otelin iletişim e-posta adresini giriniz.',
            'one_person': 'Tek kişilik odanın ücretini giriniz.',
            'two_person': 'İki kişilik odanın ücretini giriniz.',
            'tree_person': 'Üç kişilik odanın ücretini giriniz.',
            'finish': 'Fiyatın geçerlilik tarihini seçiniz.',
            'currency': 'Kullanılacak para birimini seçiniz.',
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("Otel adı boş olamaz.")
        return name
    
class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['name', 'location']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': "Etkinlik Adı",
            'location': "Konum",
        }
        help_texts = {
            'name': 'Etkinliğin adını giriniz.',
            'location': 'Etkinliğin konumunu seçiniz.',
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("Etkinlik adı boş olamaz.")
        return name

    def clean_city(self):
        city = self.cleaned_data.get('city')
        if not city:
            raise forms.ValidationError("Şehir adı boş olamaz.")
        return city
    
class MuseumForm(forms.ModelForm):
    class Meta:
        model = Museum
        fields = ['name', 'location', 'contact', 'price', 'currency']  # 'company' ve 'is_delete' kaldırıldı
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': "Müze Adı",
            'location': "Konum",
            'contact': "İletişim",
            'price': "Ücret",
            'currency': "Para Birimi",
        }
        help_texts = {
            'name': 'Müzenin adını giriniz.',
            'location': 'Müzenin bulunduğu şehri seçiniz.',
            'contact': 'Müzenin iletişim bilgilerini giriniz.',
            'price': 'Müze giriş ücretini giriniz.',
            'currency': 'Kullanılacak para birimini seçiniz.',
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("Müze adı boş olamaz.")
        return name

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise forms.ValidationError("Ücret sıfırdan küçük olamaz.")
        return price
    
class GuideForm(forms.ModelForm):
    class Meta:
        model = Guide
        fields = ['name', 'location', 'doc_no', 'phone', 'mail', 'price', 'currency']  # 'company' ve 'is_delete' kaldırıldı
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'doc_no': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'mail': forms.EmailInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': "Rehber Adı",
            'location': "Konum",
            'doc_no': "Rehber No",
            'phone': "Telefon No",
            'mail': "E-posta",
            'price': "Ücret",
            'currency': "Para Birimi",
        }
        help_texts = {
            'name': 'Rehberin adını giriniz.',
            'location': 'Rehberin bulunduğu şehirleri seçiniz.',
            'doc_no': 'Rehber numarasını giriniz.',
            'phone': 'Rehberin telefon numarasını giriniz.',
            'mail': 'Rehberin iletişim e-posta adresini giriniz.',
            'price': 'Rehberin ücretini giriniz.',
            'currency': 'Kullanılacak para birimini seçiniz.',
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("Rehber adı boş olamaz.")
        return name

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise forms.ValidationError("Ücret sıfırdan küçük olamaz.")
        return price
    
class VehicleSupplierForm(forms.ModelForm):
    class Meta:
        model = VehicleSupplier
        fields = ['name', 'location', 'contact']  # 'company' ve 'is_delete' kaldırıldı
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': "Tedarikçi Adı",
            'location': "Konum",
            'contact': "İletişim",
        }
        help_texts = {
            'name': 'Tedarikçinin adını giriniz.',
            'location': 'Tedarikçinin bulunduğu şehirleri seçiniz.',
            'contact': 'Tedarikçinin iletişim bilgilerini giriniz.',
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("Tedarikçi adı boş olamaz.")
        return name
    
class ActivitySupplierForm(forms.ModelForm):
    class Meta:
        model = Activitysupplier
        fields = ['name', 'location', 'contact']  # 'company' ve 'is_delete' kaldırıldı
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': "Etkinlik Tedarikçisi Adı",
            'location': "Konum",
            'contact': "İletişim",
        }
        help_texts = {
            'name': 'Etkinlik tedarikçisinin adını giriniz.',
            'location': 'Tedarikçinin bulunduğu şehirleri seçiniz.',
            'contact': 'Tedarikçinin iletişim bilgilerini giriniz.',
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("Tedarikçi adı boş olamaz.")
        return name
    
class ActivityCostForm(forms.ModelForm):
    class Meta:
        model = Activitycost
        fields = ['supplier', 'activity', 'price', 'currency']  # 'company' ve 'is_delete' kaldırıldı
        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'activity': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'supplier': "Aktivite Tedarikçisi",
            'activity': "Aktivite",
            'price': "Ücret",
            'currency': "Para Birimi",
        }
        help_texts = {
            'supplier': 'Tedarikçiyi seçiniz.',
            'activity': 'Aktiviteyi seçiniz.',
            'price': 'Aktivitenin ücretini giriniz.',
            'currency': 'Kullanılacak para birimini seçiniz.',
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError("Ücret sıfırdan küçük olamaz.")
        return price
    
class BuyerCompanyForm(forms.ModelForm):
    class Meta:
        model = Buyercompany
        fields = ['name', 'short_name', 'contact']  # 'company' ve 'is_delete' kaldırıldı
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'short_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': "Şirket Adı",
            'short_name': "Kısa Adı",
            'contact': "İletişim",
        }
        help_texts = {
            'name': 'Şirketin adını giriniz.',
            'short_name': 'Şirketin kısa adını giriniz.',
            'contact': 'Şirketin iletişim bilgilerini giriniz.',
        }

    def clean_short_name(self):
        short_name = self.cleaned_data.get('short_name')
        if not short_name:
            raise forms.ValidationError("Kısa adı boş olamaz.")
        return short_name
    
from django import forms
from .models import Vehiclecost

class VehicleCostForm(forms.ModelForm):
    class Meta:
        model = Vehiclecost
        fields = ['supplier', 'tour', 'transfer']  # İstediğiniz alanları buraya ekleyin
        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'tour': forms.Select(attrs={'class': 'form-control'}),
            'transfer': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'supplier': "Tedarikçi",
            'tour': "Tur",
            'transfer': "Transfer",
        }
        help_texts = {
            'supplier': 'Tedarikçiyi seçiniz.',
            'tour': 'İlgili turu seçiniz (varsa).',
            'transfer': 'İlgili transferi seçiniz (varsa).',
        }

    def clean(self):
        cleaned_data = super().clean()
        # Ek temizlik ve doğrulama işlemleri buraya eklenebilir
        return cleaned_data


class VehicleCostPriceForm(forms.ModelForm):
    class Meta:
        model = VehicleCostPrice
        fields = ['vehicle_cost', 'vehicle', 'price', 'currency']  # İstediğiniz alanları buraya ekleyin
        widgets = {
            'vehicle_cost': forms.Select(attrs={'class': 'form-control'}),
            'vehicle': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'vehicle_cost': "Araç Maliyeti",
            'vehicle': "Araç",
            'price': "Fiyat",
            'currency': "Para Birimi",
        }
        help_texts = {
            'vehicle_cost': 'Araç maliyetini seçiniz.',
            'vehicle': 'Araç seçiniz.',
            'price': 'Araç için fiyatı giriniz.',
            'currency': 'Fiyatın para birimini seçiniz.',
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Fiyat sıfırdan büyük olmalıdır.")
        return price
    

class BuyercompanyForm(forms.ModelForm):
    class Meta:
        model = Buyercompany
        fields = ['branch', 'name', 'short_name', 'contact']
        widgets = {
            'branch': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'short_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'branch': 'Branch',
            'name': 'Name',
            'short_name': 'Short Name',
            'contact': 'Contact',
        }