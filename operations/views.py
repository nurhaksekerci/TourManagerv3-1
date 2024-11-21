from django.shortcuts import get_object_or_404, render, redirect
from .forms import *
from .models import *
from company.models import *
from datetime import date, timedelta
from django.shortcuts import render, redirect
from django.forms import BaseFormSet, inlineformset_factory
from django.http import HttpResponse
from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required  
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
            context = {
                'day': day,
                'title': day.operation.ticket,
            }
            return render(request, 'main/includes/operations/operation_day_items.html', context)  # Başarılı kayıttan sonra yönlendirme yapılacak sayfa

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

@login_required  
def create_item_detail(request, day_id):
    day = OperationDay.objects.get(id=day_id)
    context = {
        'day': day,
        'title': day.operation.ticket,
    }
    return render(request, 'main/pages/operations/operation_day_items.html', context)

@login_required  
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

@login_required  
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

@login_required  
def save_all_forms(request, day_id):
    day = OperationDay.objects.get(id=day_id)
    if request.method == 'POST':
        item_forms = []
        sub_item_forms = []
        saved_items = {}
        form_errors = False
        processed_items = set()
        processed_sub_items = set()

        for key, value in request.POST.items():
            if key.startswith('create_vehicle_') or key.startswith('create_walking_tour_') or key.startswith('create_walking_activity_'):
                prefix = key.split('-')[0]
                item_no = int(prefix.split('_')[-1])
                item_type = prefix.rsplit('_', 1)[0]
                if item_no in processed_items:
                    continue

                form = DynamicOperationItemForm(request.POST, prefix=prefix, item_type=item_type, item_no=item_no, request=request)
                if item_type == "vehicle" or item_type == "create_vehicle":
                    item_title = "Vehicle"
                elif item_type == "walking_tour" or item_type == "create_walking_tour":
                    item_title = "Walking Tour"
                elif item_type == "walking_activity" or item_type == "create_walking_activity":
                    item_title = "Walking Activity"
                    
                if form.is_valid():
                    item_instance = form.save(commit=False)
                    item_instance.operation_day = day
                    item_instance.item_type = item_title
                    item_instance.save()
                    saved_items[item_no] = item_instance
                    item_forms.append(form)
                    processed_items.add(item_no)
                else:
                    form_errors = True
                    print("Ana item form errors:", form.errors)

            if key.startswith('create_other_price_') or key.startswith('create_guide_') or key.startswith('create_museum_') or \
               key.startswith('create_activity_') or key.startswith('create_hotel_') or key.startswith('create_transfer_') or \
               key.startswith('create_tour_'):
                prefix = key.split('-')[0]  # '-' karakterinden önceki kısmı alıyoruz
                sub_item_type = prefix.rsplit('_', 2)[0]  # sub_item_type kısmını belirliyoruz
                item_no = int(prefix.split('_')[-2])  # item_no değerini alıyoruz
                sub_item_no = int(prefix.split('_')[-1])  # sub_item_no değerini alıyoruz

                if (item_no, sub_item_no) in processed_sub_items:
                    continue

                sub_prefix = f"{sub_item_type}_{item_no}_{sub_item_no}"


                sub_form = DynamicOperationSubItemForm(request.POST, prefix=sub_prefix, sub_item_type=sub_item_type, sub_item_no=sub_item_no, request=request)
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


                if sub_form.is_valid():
                    sub_item_instance = sub_form.save(commit=False)
                    sub_item_instance.operation_item = saved_items.get(item_no)
                    sub_item_instance.sub_item_type = sub_item_title
                    sub_item_instance.save()
                    sub_item_forms.append(sub_form)
                    processed_sub_items.add((item_no, sub_item_no))
                else:
                    form_errors = True
                    print("Alt item form errors:", sub_form.errors)

        if form_errors:
            return HttpResponse(status=400)

        for form in item_forms:
            form.save()
        for sub_form in sub_item_forms:
            sub_form.save()

        next_day = OperationDay.objects.filter(date__gt=day.date, operation=day.operation, is_delete=False).order_by('date').first()
        if next_day:
            context = {
                'day': next_day,
                'title': day.operation.ticket,
            }
            return render(request, 'main/includes/operations/operation_day_items.html', context)

    return HttpResponse(status=200)


@login_required
def update_operation_item(request, pk, item_type):
    # `create_` ile başlayan item_type'leri reddet
    if item_type.startswith('create_'):
        return JsonResponse({'error': 'Güncelleme işlemi sadece mevcut item_type için yapılabilir.'}, status=400)

    # Güncellenmekte olan OperationItem kaydını al
    operation_item = get_object_or_404(OperationItem, pk=pk, is_delete=False)

    # JSON'dan alınan attributes'u doldurma
    initial_data = operation_item.attributes or {}
    
    if request.method == 'POST':
        # Formu POST verisi ile doldur
        form = DynamicOperationItemForm(
            request.POST,
            instance=operation_item,
            item_type=item_type,
            request=request
        )
        if form.is_valid():
            item = form.save()

            job_attributes = item.attributes
            if item.item_type == 'Vehicle':
                vehicle_id = job_attributes.get('vehicle_type')
                if vehicle_id:
                    vehicle = Vehicle.objects.filter(id=vehicle_id).first()
                    job_attributes['vehicle_type'] = vehicle.vehicle if vehicle else "Unknown Vehicle"
            elif item.item_type == 'Walking Tour':
                tour_id = job_attributes.get('tour')
                if tour_id:
                    tour = NoVehicleTour.objects.filter(id=tour_id).first()
                    job_attributes['tour'] = tour.route if tour else "Unknown Tour"
            elif item.item_type == 'Walking Activity':
                activity_id = job_attributes.get('activity')
                if activity_id:
                    activity = Activity.objects.filter(id=activity_id).first()
                    job_attributes['activity'] = activity.name if activity else "Unknown Activity"
            job = {
                "job_id": item.id,
                "item_type": item.item_type,
                "attributes": job_attributes,
                "order": item.order,
            }

            context = {
                'title': 'TEST',
                'job': job,
            }

            return render(request, 'main/includes/operations/job_item.html', context)

        else:
            return render(request, 'main/includes/operations/job_item_update.html', {
                'form': form,
                'operation_item': operation_item,
                'item_type': item_type
            })
    else:
        # GET isteği: JSON alanlarını initial olarak forma yükle
        form = DynamicOperationItemForm(
            instance=operation_item,
            initial=initial_data,  # attributes JSON'u başlangıç verisi olarak kullanılıyor
            item_type=item_type,
            request=request
        )
        return render(request, 'main/includes/operations/job_item_update.html', {
            'form': form,
            'operation_item': operation_item,
            'item_type': item_type
        })



@login_required
def update_operation_sub_item(request, pk, sub_item_type):
    # `create_` ile başlayan sub_item_type'leri reddet
    if sub_item_type.startswith('create_'):
        return JsonResponse({'error': 'Güncelleme işlemi sadece mevcut sub_item_type için yapılabilir.'}, status=400)

    # Güncellenmekte olan OperationSubItem kaydını al
    sub_item = get_object_or_404(OperationSubItem, pk=pk, is_delete=False)

    # JSON'dan alınan attributes'u doldurma
    initial_data = sub_item.attributes or {}
    
    if request.method == 'POST':
        # Formu POST verisi ile doldur
        form = DynamicOperationSubItemForm(
            request.POST,
            instance=sub_item,
            sub_item_type=sub_item_type,
            request=request
        )
        if form.is_valid():
            if hasattr(form, 'save_m2m'):  # save_m2m metodu mevcut mu kontrol edin
                form.save_m2m()
            item = form.save()
            attributes = sub_item.attributes
            if sub_item.sub_item_type in ['Tour', 'Transfer']:
                model = Tour if sub_item.sub_item_type == 'Tour' else Transfer
                related_object = model.objects.filter(id=attributes.get(sub_item.sub_item_type.lower())).first()
                attributes[f'{sub_item.sub_item_type.lower()}'] = related_object.route if related_object else "Unknown Route"
            else:
                model = {
                    'hotel': Hotel,
                    'activity': Activity,
                    'museum': Museum,
                    'guide': Guide,
                }.get(sub_item.sub_item_type.lower(), None)
                
                if sub_item.sub_item_type.lower() != "other price":
                    related_object = model.objects.filter(id=attributes.get(sub_item.sub_item_type.lower())).first() if model else None
                    attributes[f'{sub_item.sub_item_type.lower()}'] = related_object.name if related_object else "Unknown Name"
            context = {
                "sub_item": {
                    "sub_item_id": item.id,
                    "sub_item_type": item.sub_item_type,
                    "attributes": item.attributes if item.attributes else {},
                    "order": item.order,
                },
                'sub_item_type': item.sub_item_type
            }
            return render(request, 'main/includes/operations/job_sub_item.html', context)
        else:
            return render(request, 'main/includes/operations/job_sub_item_update.html', {
                'form': form,
                'sub_item': sub_item,
                'sub_item_type': sub_item_type
            })
    else:
        # GET isteği: JSON alanlarını initial olarak forma yükle
        form = DynamicOperationSubItemForm(
            instance=sub_item,
            initial=initial_data,  # attributes JSON'u başlangıç verisi olarak kullanılıyor
            sub_item_type=sub_item_type,
            request=request
        )
        return render(request, 'main/includes/operations/job_sub_item_update.html', {
            'form': form,
            'sub_item': sub_item,
            'sub_item_type': sub_item_type
        })
    
@login_required   
def jobs(request):
    employee = Employee.objects.get(user=request.user)
    today = date.today()
    next_three_days = [today + timedelta(days=i) for i in range(3)]
    
    # Günlere göre OperationDay'leri gruplama
    operation_days_by_date = {day: [] for day in next_three_days}

    # İlgili OperationDay'leri al
    operation_days = OperationDay.objects.filter(
        date__in=next_three_days,
        is_delete=False,
        branch = employee.branch
    ).order_by('date').select_related('operation')

    for operation_day in operation_days:
        ticket = operation_day.operation.ticket
        jobs = operation_day.operation_items.filter(is_delete=False)

        job_list = []
        for job in jobs:
            job_attributes = job.attributes
            if job.item_type == 'Vehicle':
                vehicle_id = job_attributes.get('vehicle_type')
                if vehicle_id:
                    vehicle = Vehicle.objects.filter(id=vehicle_id).first()
                    job_attributes['vehicle_type'] = vehicle.vehicle if vehicle else "Unknown Vehicle"
            elif job.item_type == 'Walking Tour':
                tour_id = job_attributes.get('tour')
                if tour_id:
                    tour = NoVehicleTour.objects.filter(id=tour_id).first()
                    job_attributes['tour'] = tour.route if tour else "Unknown Tour"
            elif job.item_type == 'Walking Activity':
                activity_id = job_attributes.get('activity')
                if activity_id:
                    activity = Activity.objects.filter(id=activity_id).first()
                    job_attributes['activity'] = activity.name if activity else "Unknown Activity"

            sub_items = job.sub_items.filter(is_delete=False)

            # Sub Items'i türüne göre gruplama ve attributes'u işleme
            grouped_sub_items = defaultdict(list)
            for sub_item in sub_items:
                attributes = sub_item.attributes

                # sub_item_type'e göre route veya name belirleme ve attributes'u güncelleme
                if sub_item.sub_item_type in ['Tour', 'Transfer']:
                    model = Tour if sub_item.sub_item_type == 'Tour' else Transfer
                    related_object = model.objects.filter(id=attributes.get(sub_item.sub_item_type.lower())).first()
                    attributes[f'{sub_item.sub_item_type.lower()}'] = related_object.route if related_object else "Unknown Route"
                else:
                    model = {
                        'hotel': Hotel,
                        'activity': Activity,
                        'museum': Museum,
                        'guide': Guide,
                    }.get(sub_item.sub_item_type.lower(), None)
                    
                    if sub_item.sub_item_type.lower() != "other price":
                        related_object = model.objects.filter(id=attributes.get(sub_item.sub_item_type.lower())).first() if model else None
                        attributes[f'{sub_item.sub_item_type.lower()}'] = related_object.name if related_object else "Unknown Name"

                # İşlenmiş attributes'u grouped_sub_items'e ekleme
                grouped_sub_items[sub_item.sub_item_type].append({
                    "sub_item_id": sub_item.id,
                    "attributes": attributes,
                    "order": sub_item.order,
                })

            job_list.append({
                "job_id": job.id,
                "item_type": job.item_type,
                "attributes": job.attributes,
                "order": job.order,
                "grouped_sub_items": dict(grouped_sub_items)  # dict'e dönüştürme
            })

        operation_days_by_date[operation_day.date].append({
            "operation_day": operation_day,
            "ticket": ticket,
            "jobs": job_list
        })

    return render(request, 'main/pages/operations/jobs.html', {'operation_days_by_date': operation_days_by_date})

