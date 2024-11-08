# myapp/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_item(obj, field):
    if isinstance(obj, dict):
        return obj.get(field)  # Sözlükte anahtar ile al
    return getattr(obj, field, None)  # Diğer nesneler için getattr kullan

