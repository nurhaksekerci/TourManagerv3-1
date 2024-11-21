from django.shortcuts import render
from company.models import *
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Employee  # Gerekli model importu

@login_required
def generic_view(request, model):
    employee = get_object_or_404(Employee, user=request.user)
    branch = employee.branch

    # Model sınıfını dinamik olarak al
    ModelClass = globals().get(model)
    if not ModelClass:
        return render(request, '404.html', {'error': 'Model not found'})
    
    queryset = ModelClass.objects.filter(branch=branch).order_by("is_delete")

    counts = queryset.values('is_delete').annotate(count=models.Count('id'))
    deleted_count = next((item['count'] for item in counts if item['is_delete']), 0)
    active_count = next((item['count'] for item in counts if not item['is_delete']), 0)
    all_count = queryset.count()
    FormClass = globals().get(f"{model}Form")
    form = FormClass() if FormClass else None

    fields = ModelClass._meta.fields
    objects_data = [
        {field.name: getattr(obj, field.name) for field in fields}
        for obj in queryset
    ]


    context = {
        'title': model,
        'deleted_count': deleted_count,
        'active_count': active_count,
        'all_count': all_count,
        'form': form,
        'objects_data': objects_data,
        'models': queryset,  # Model nesneleri
        'fields': [field.name for field in fields],
        'field_labels': [field.verbose_name.capitalize() for field in fields],  # Alan isimleri
        'model_name': model,
    }

    return render(request, 'main/pages/generic.html', context)


@login_required
def generic_create_view(request, model):
    request_personnel = Employee.objects.get(user=request.user)
    branch = request_personnel.branch
    model_class = globals().get(model)
    if model_class is None:
        return HttpResponseNotFound(f"{model} model not found")
    form_class = globals().get(f"{model}Form")
    if form_class is None:
        return HttpResponseNotFound(f"{model}Form not found")
    if request.method == "POST":
        form = form_class(request.POST or None)
        if form.is_valid():
            new_object = form.save(commit=False)
            new_object.branch = branch
            if model == "Notification":
                new_object.sender = request_personnel
            form.save_m2m()
            new_object.save()
            action_description = f"{model} oluşturdu. ID: {new_object.id}"
            log = UserActivityLog(
                branch=branch,
                staff=request_personnel,
                action=action_description
            )
            log.save()
            obj_data = {'id': new_object.id}
            for field in model_class._meta.fields:
                obj_data[field.name] = getattr(new_object, field.name)
            context = {
                'fields': [field.name for field in model_class._meta.fields],  # alan adlarını dahil et
                'obj': obj_data,
                'model_name': model
            }
            return render(request, 'main/includes/generic/generic-list.html', context)
        else:
            errors = form.errors.as_json()
            action_description = f"{model} Kayıt Oluşturulamadı. Hata: " + errors
            log = UserActivityLog(
                branch=branch,
                staff=request_personnel,
                action=action_description
            )
            log.save()
    else:
        form = form_class()
    context = {
        'form': form,
        'model_name': model
    }
    return render(request, 'main/includes/generic/generic-form.html', context)

@login_required
def generic_edit_view(request, model, obj_id):
    ModelClass = globals().get(model)
    if ModelClass is None:
        return HttpResponseNotFound(f"{model} model not found.")
    obj = get_object_or_404(ModelClass, id=obj_id)
    request_personnel = Employee.objects.get(user=request.user)
    branch = request_personnel.branch
    FormClass = globals().get(f"{model}Form")
    if FormClass is None:
        return HttpResponseNotFound(f"{model}Form not found.")
    if request.method == "POST":
        original_data = {field.name: getattr(obj, field.name) for field in ModelClass._meta.fields}
        form = FormClass(request.POST, instance=obj)
        if form.is_valid():
            if hasattr(form, 'save_m2m'):  # save_m2m metodu mevcut mu kontrol edin
                form.save_m2m()
            updated_obj = form.save()
            updated_data = {field.name: getattr(updated_obj, field.name) for field in ModelClass._meta.fields}
            changes = [
                f"{key}: {original_data[key]} den {updated_data[key]} ye değişti"
                for key in original_data if original_data[key] != updated_data[key]
            ]
            if changes:
                action_description = f"Güncellendi. {model} {obj_id}: " + ", ".join(changes)
                log = UserActivityLog(
                    branch=branch,
                    staff=request_personnel,
                    action=action_description
                )
                log.save()
            obj_data = {'id': obj_id}  # ID bilgisini ekleyin
            for field in ModelClass._meta.fields:
                obj_data[field.name] = getattr(obj, field.name)
            context = {
                'form': form,
                'obj': obj_data,  # Güncellenmiş obje verileri
                'model_name': model,
                'fields': [field.name for field in ModelClass._meta.fields],
            }
            return render(request, 'main/includes/generic/generic-list.html', context)
    else:
        form = FormClass(instance=obj)
        context = {
            'form': form,
            'obj': obj,  # Form başlangıcında objeyi gönder
            'model_name': model,
            'fields': [field.name for field in ModelClass._meta.fields],
        }
    return render(request, 'main/includes/generic/generic-edit-form.html', context)

@login_required
def generic_delete_view(request, model, obj_id):
    ModelClass = globals().get(model)
    if ModelClass is None:
        return HttpResponseNotFound(f"{model} model not found.")
    obj = get_object_or_404(ModelClass, id=obj_id)
    request_personnel = Employee.objects.get(user=request.user)
    branch = request_personnel.branch
    if request.method == "POST":
        obj_data = {field.name: getattr(obj, field.name) for field in ModelClass._meta.fields}
        item = get_object_or_404(ModelClass, id=obj_id)
        
        try:
            item.is_delete = True
            item.save()

            action_description = f"Silindi {model} {obj_id}: " + ", ".join([f"{key}: {value}" for key, value in obj_data.items()])
            log = UserActivityLog(
                branch=branch,
                staff=request_personnel,
                action=action_description
            )
            log.save()

            context = {
                'obj': item,  # Güncellenmiş obje
                'model_name': model,
                'fields': [field.name for field in ModelClass._meta.fields],
            }
            return render(request, 'main/includes/generic/generic-list.html', context)
        except ModelClass.DoesNotExist:
            return HttpResponseNotFound(f"{model} not found.")
        
@login_required
def generic_reload_view(request, model, obj_id):
    ModelClass = globals().get(model)
    if ModelClass is None:
        return HttpResponseNotFound(f"{model} model not found.")
    obj = get_object_or_404(ModelClass, id=obj_id)
    request_personnel = Employee.objects.get(user=request.user)
    branch = request_personnel.branch
    if request.method == "POST":
        obj_data = {field.name: getattr(obj, field.name) for field in ModelClass._meta.fields}
        item = get_object_or_404(ModelClass, id=obj_id)
        
        try:
            item.is_delete = False
            item.save()

            action_description = f"Geri yüklendi: {model} {obj_id}: " + ", ".join([f"{key}: {value}" for key, value in obj_data.items()])
            log = UserActivityLog(
                branch=branch,
                staff=request_personnel,
                action=action_description
            )
            log.save()

            context = {
                'obj': item,  # Güncellenmiş obje
                'model_name': model,
                'fields': [field.name for field in ModelClass._meta.fields],
            }
            return render(request, 'main/includes/generic/generic-list.html', context)
        except ModelClass.DoesNotExist:
            return HttpResponseNotFound(f"{model} not found.")


@login_required
def generic_cancel_view(request, model, obj_id):
    ModelClass = globals().get(model)
    if ModelClass is None:
        return HttpResponseNotFound(f"{model} model not found.")
    obj = get_object_or_404(ModelClass, id=obj_id)
    obj_data = {'id': obj_id}
    for field in ModelClass._meta.fields:
        obj_data[field.name] = getattr(obj, field.name)
    return render(request, 'main/includes/generic/generic-list.html', {'obj': obj_data, 'fields': [field.name for field in ModelClass._meta.fields], 'model_name': model,})