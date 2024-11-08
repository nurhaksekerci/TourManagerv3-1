# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from company.models import *

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='Email, Username, or Phone', max_length=150)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            # Kullanıcıyı e-posta veya telefon numarasına göre bul
            user = CustomUser.objects.get(email=username) or CustomUser.objects.get(phone=username)
            return user.username  # Kullanıcı adını döndür
        except CustomUser.DoesNotExist:
            raise forms.ValidationError("No account found with this email or phone number.")


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'name',
            'city',
            'district',
            'neighborhood',
            'address',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'district': forms.Select(attrs={'class': 'form-control'}),
            'neighborhood': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Address', 'rows': 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.all()
        self.fields['district'].queryset = District.objects.none()  # İlk başta boş
        self.fields['neighborhood'].queryset = Neighborhood.objects.none()  # İlk başta boş

        if 'city' in self.data:
            try:
                city_id = int(self.data.get('city'))
                self.fields['district'].queryset = District.objects.filter(city_id=city_id).order_by('name')
            except (ValueError, TypeError):
                pass  # Invalid input, ignore

        if 'district' in self.data:
            try:
                district_id = int(self.data.get('district'))
                self.fields['neighborhood'].queryset = Neighborhood.objects.filter(district_id=district_id).order_by('name')
            except (ValueError, TypeError):
                pass

from django.contrib.auth.forms import UserCreationForm
class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'gender', 'username', 'email', 'phone', 'password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Re-enter Password'}),
        }