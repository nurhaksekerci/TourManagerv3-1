from django import forms
from .models import EgitimPlan

class EgitimPlanForm(forms.ModelForm):
    class Meta:
        model = EgitimPlan
        fields = ['name', 'phone', 'egitmen', 'day']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'egitmen': forms.Select(attrs={'class': 'form-control'}),
            'day': forms.Select(attrs={'class': 'form-control'}),
        }
