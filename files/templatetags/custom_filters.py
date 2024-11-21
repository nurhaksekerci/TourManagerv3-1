# myapp/templatetags/custom_filters.py
from django import template
from itertools import groupby
from operator import itemgetter
from django.apps import apps

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




@register.filter
def groupby(value, key):
    """
    Verilen veri kümesini belirtilen bir anahtara göre gruplar.
    Kullanım: {% for key, group in data|groupby_key:'key_name' %}
    """
    try:
        sorted_value = sorted(value, key=itemgetter(key))  # Anahtara göre sırala
        return groupby(sorted_value, key=itemgetter(key))  # Anahtara göre gruplandır
    except (TypeError, KeyError):
        return []

related_fields = {
    'tour': 'files.Tour',
    'hotel': 'files.Hotel',
    'activity': 'files.Activity',
    'museum': 'files.Museum',
    'transfer': 'files.Transfer',
    'guide': 'files.Guide',
}

@register.filter
def lookup_by_id(object_id, model_name):
    Model = apps.get_model(model_name)
    if Model:
        try:
            instance = Model.objects.get(id=object_id)
            return getattr(instance, 'name', getattr(instance, 'route', "Tanımsız"))
        except Model.DoesNotExist:
            return "Bilinmiyor"
    return "Geçersiz Model"

@register.filter
def get_related_model(related_fields, sub_item_type):
    return related_fields.get(sub_item_type)
