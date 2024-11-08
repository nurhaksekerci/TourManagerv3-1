from django.http import JsonResponse
from django.shortcuts import render,redirect
from .models import EgitimPlan
from .forms import EgitimPlanForm

def egitim_plan_view(request):
    form = EgitimPlanForm()

    if request.method == 'POST':
        form = EgitimPlanForm(request.POST)
        if form.is_valid():
            # Form geçerli, veritabanına kaydediyoruz
            form.save()
            # Başarı mesajı ve yönlendirme
            return redirect('auth_login')  # Başarı sonrası yönlendirme
        else:
            # Eğer form geçersizse hata mesajlarını formda göster
            return render(request, 'educations/egitim_plan_form.html', {'form': form})
    
    # Eğer GET isteği ise formu boş olarak göster
    return render(request, 'educations/egitim_plan_form.html', {'form': form})

def get_available_days(request):
    # AJAX isteğini kontrol etmek için 'X-Requested-With' başlığını kontrol et
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        egitmen_id = request.GET.get('egitmen_id')
        
        # Eğer egitmen_id yoksa, 400 hatası döndürelim
        if not egitmen_id:
            return JsonResponse({'error': 'Eğitmen ID eksik'}, status=400)

        try:
            # Eğitmenin daha önce seçilmiş olduğu günleri bulalım
            selected_days = EgitimPlan.objects.filter(egitmen_id=egitmen_id).values_list('day', flat=True)
            
            # Gün seçeneklerini oluştur
            all_days = ['13', '14', '15', '18', '19', '20']
            available_days = [day for day in all_days if day not in selected_days]
            
            # Boş günleri JSON formatında döndürelim
            return JsonResponse({'available_days': available_days})
        except Exception as e:
            # Eğer bir hata oluşursa, hata mesajını JSON formatında döndürelim
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)
