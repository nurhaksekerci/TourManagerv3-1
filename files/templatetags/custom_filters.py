# myapp/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_item(obj, field):
    if isinstance(obj, dict):
        return obj.get(field)  # Sözlükte anahtar ile al
    return getattr(obj, field, None)  # Diğer nesneler için getattr kullan

@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})

@register.filter(name='add_class2')
def add_class2(field, css_class):
    """
    Form alanına bir CSS sınıfı ekler.
    """
    if hasattr(field, 'as_widget'):  # Alanın bir widget olduğunu kontrol ediyoruz
        return field.as_widget(attrs={'class': css_class})
    return field  