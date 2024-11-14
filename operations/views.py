from django.shortcuts import get_object_or_404, render, redirect
from .forms import *
from .models import *
from company.models import *
from datetime import timedelta
from django.shortcuts import render, redirect
from django.forms import BaseFormSet, formset_factory, inlineformset_factory, modelformset_factory
from datetime import timedelta
from django.http import HttpResponse


def operation_create(request):
    employee = Employee.objects.get(user=request.user)
    branch = employee.branch

    # Form ve Formsetleri ayarla
    CustomerFormSet = inlineformset_factory(Operation, Customer, form=CustomerForm, extra=1, can_delete=True)
    SalesPriceFormSet = inlineformset_factory(Operation, SalesPrice, form=SalesPriceForm, extra=1, can_delete=True)

    if request.method == 'POST':
        operation_form = OperationForm(request.POST)
        customer_formset = CustomerFormSet(request.POST, prefix='customers')
        salesprice_formset = SalesPriceFormSet(request.POST, prefix='salesprices')

        if operation_form.is_valid() and customer_formset.is_valid() and salesprice_formset.is_valid():
            operation = operation_form.save(commit=False)
            operation.branch = branch
            operation.create_employee = employee
            operation.save()

            # Operation için günleri oluştur
            current_date = operation.start_at
            end_date = operation.finish_at
            while current_date <= end_date:
                OperationDay.objects.create(
                    branch=operation.branch,
                    operation=operation,
                    date=current_date
                )
                current_date += timedelta(days=1)

            customer_formset.instance = operation
            customer_formset.save()
            salesprice_formset.instance = operation
            salesprice_formset.save()

            day = OperationDay.objects.filter(operation=operation).first()
            return redirect('create_operation_items', day_id = day.id)  # Başarılı kayıttan sonra yönlendirme yapılacak sayfa

    else:
        operation_form = OperationForm()
        customer_formset = CustomerFormSet(prefix='customers')
        salesprice_formset = SalesPriceFormSet(prefix='salesprices')

    context = {
        'title': 'Operation Create',
        'form': operation_form,
        'customer_formset': customer_formset,
        'salesprice_formset': salesprice_formset,
    }
    return render(request, 'main/pages/operations/operation_create.html', context)


class DynamicOperationSubItemFormSet(BaseFormSet):
    def __init__(self, *args, sub_item_type=None, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.sub_item_type = sub_item_type
        self.request = request

    def _construct_form(self, i, **kwargs):
        kwargs['sub_item_type'] = self.sub_item_type
        kwargs['request'] = self.request
        return super()._construct_form(i, **kwargs)


def create_item_detail(request, day_id):
    day = OperationDay.objects.get(id=day_id)
    context = {
        'day': day,
        'title': day.operation.ticket,
    }
    return render(request, 'main/pages/operations/operation_day_items.html', context)


def create_items(request, day_id, item_type, item_no):
    day = OperationDay.objects.get(id=day_id)
    prefix = f"{item_type}_{item_no}"
    item_form = DynamicOperationItemForm(request.POST or None, item_type=item_type, item_no=item_no, request=request, prefix=prefix)
    if item_type == "vehicle" or item_type == "create_vehicle":
        item_title = "Vehicle"
    elif item_type == "walking_tour" or item_type == "create_walking_tour":
        item_title = "Walking Tour"
    elif item_type == "walking_activity" or item_type == "create_walking_activity":
        item_title = "Walking Activity"

    vehicle_sub_items = [
        {'type': 'create_tour', 'icon': 'fa-map-location-dot', 'title': 'Tour'},
        {'type': 'create_transfer', 'icon': 'fa-taxi', 'title': 'Transfer'},
        {'type': 'create_hotel', 'icon': 'fa-hotel', 'title': 'Hotel'},
        {'type': 'create_activity', 'icon': 'fa-person-skiing', 'title': 'Activity'},
        {'type': 'create_museum', 'icon': 'fa-landmark', 'title': 'Museum'},
        {'type': 'create_guide', 'icon': 'fa-person-walking-luggage', 'title': 'Guide'},
        {'type': 'create_other_price', 'icon': 'fa-hand-holding-dollar', 'title': 'Other Price'}
    ]
    tour_sub_items = [
        {'type': 'create_museum', 'icon': 'fa-landmark', 'title': 'Museum'},
        {'type': 'create_guide', 'icon': 'fa-person-walking-luggage', 'title': 'Guide'},
        {'type': 'create_other_price', 'icon': 'fa-hand-holding-dollar', 'title': 'Other Price'}
    ]
    activity_sub_items = [
        {'type': 'create_guide', 'icon': 'fa-person-walking-luggage', 'title': 'Guide'},
        {'type': 'create_other_price', 'icon': 'fa-hand-holding-dollar', 'title': 'Other Price'}
    ]

    context = {
        
        'item_type': item_type,
        'item_title': item_title,
        'day': day,
        'item_form': item_form,
        'item_no': item_no,
        'vehicle_sub_items': vehicle_sub_items,
        'tour_sub_items': tour_sub_items,
        'activity_sub_items': activity_sub_items,

    }
    return render(request, 'main/includes/operations/create_items.html', context)

def create_sub_items(request, day_id, item_type, sub_item_type, sub_item_no, item_no):
    day = OperationDay.objects.get(id=day_id)
    prefix = f"{sub_item_type}_{item_no}_{sub_item_no}"
    sub_item_form = DynamicOperationSubItemForm(request.POST or None, sub_item_type=sub_item_type, sub_item_no=sub_item_no, request=request, prefix=prefix)
    if sub_item_type == "tour" or sub_item_type == "create_tour":
        sub_item_title = "Tour"
    elif sub_item_type == "transfer" or sub_item_type == "create_transfer":
        sub_item_title = "Transfer"
    elif sub_item_type == "hotel" or sub_item_type == "create_hotel":
        sub_item_title = "Hotel"
    elif sub_item_type == "activity" or sub_item_type == "create_activity":
        sub_item_title = "Activity"
    elif sub_item_type == "museum" or sub_item_type == "create_museum":
        sub_item_title = "Museum"
    elif sub_item_type == "guide" or sub_item_type == "create_guide":
        sub_item_title = "Guide"
    elif sub_item_type == "other_price" or sub_item_type == "create_other_price":
        sub_item_title = "Other Price"
    else:
        sub_item_title = "None"
    context = {
        'day': day,
        'sub_item_title': sub_item_title,
        'sub_item_type': sub_item_type,
        'sub_item_form': sub_item_form,
        'item_type': item_type,
        'sub_item_no': sub_item_no,
        'item_no': item_no,
    }
    return render(request, 'main/includes/operations/create_sub_items.html', context)

def save_all_forms(request, day_id):
    day = OperationDay.objects.get(id=day_id)
    if request.method == 'POST':
        item_forms = []
        saved_items = {}
        form_errors = False
        processed_items = {}

        # Sadece `item_no` değerini almak için `split` düzenlemesi
        for key, value in request.POST.items():
            if key.startswith('create_vehicle_') or key.startswith('create_walking_tour_') or key.startswith('create_walking_activity_'):
                parts = key.split('_')
                if len(parts) > 2 and parts[0] == 'create':
                    item_type = '_'.join(parts[:2]) if parts[1] == 'vehicle' else '_'.join(parts[:3])
                    item_no = parts[-1].split('-')[0]  # Sadece `item_no` sayısını alıyoruz
                    
                    print("Processing key:", key)  # Debug için
                    print("Extracted item_type:", item_type)  # Debug için
                    print("Extracted item_no:", item_no)  # Debug için

                    if item_no in processed_items:
                        continue
                
                # Prefix tam olarak POST verisindeki anahtarlarla eşleşmeli
                prefix = f"{item_type}_{item_no}"
                print("Prefix:", prefix)  # Prefix değerini kontrol et

                form = DynamicOperationItemForm(request.POST, prefix=prefix, item_type=item_type, item_no=item_no, request=request)
                
                if form.is_valid():
                    item_instance = form.save(commit=False)
                    item_instance.operation_day = day
                    item_instance.item_type = item_type
                    item_instance.save()
                    saved_items[item_no] = item_instance
                    item_forms.append(form)
                    processed_items[item_no] = True
                else:
                    form_errors = True
                    print("Form errors:", form.errors)

        if form_errors:
            return HttpResponse(status=400)

        for form in item_forms:
            form.save()

        return HttpResponse(status=200)

