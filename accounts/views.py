# views.py
from django.contrib.auth import login
from django.shortcuts import render, redirect
from company.models import CustomUser
from .forms import *
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def auth_login(request):
    if request.method == 'POST':
        email_or_username = request.POST.get('email_or_username')
        password = request.POST.get('password')
        
        try:
            # Kullanıcıyı e-posta veya telefon numarasına göre bul
            user = CustomUser.objects.get(email=email_or_username)  # E-posta ile bul
        except CustomUser.DoesNotExist:
            try:
                user = CustomUser.objects.get(phone=email_or_username)  # Telefon numarası ile bul
            except CustomUser.DoesNotExist:
                try:
                    user = CustomUser.objects.get(username=email_or_username)  # Kullanıcı adı ile bul
                except CustomUser.DoesNotExist:
                    user = None

        # Kullanıcıyı kimlik doğrulama
        if user is not None and user.check_password(password):
            login(request, user)
            return redirect('my_profile')  # Başarılı girişten sonra yönlendirme
        else:
            error_message = "Invalid email/username/phone or password."
            return render(request, 'accounts/pages/login.html', {'error_message': error_message})
    
    return render(request, 'accounts/pages/login.html')


def load_districts(request):
    city_id = request.GET.get('city_id')
    districts = District.objects.filter(city_id=city_id).order_by('name')
    return JsonResponse(list(districts.values('id', 'name')), safe=False)

def load_neighborhoods(request):
    district_id = request.GET.get('district_id')
    neighborhoods = Neighborhood.objects.filter(district_id=district_id).order_by('name')
    return JsonResponse(list(neighborhoods.values('id', 'name')), safe=False)


def auth_company_register(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save()
            branch = Branch.objects.create(company=company, name="Main", city=company.city, district=company.district, neighborhood=company.neighborhood, address=company.address)
            return redirect('auth_employee_register', slug = branch.slug)
    else:
        form = CompanyForm()

    return render(request, 'accounts/pages/company_register.html', {'form': form})


def auth_employee_register(request, slug):
    branch = Branch.objects.get(slug=slug)
    
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()  # Kullanıcıyı kaydet
            employee = Employee.objects.create(user=user, branch=branch, is_manager=True)
            send_verification_email(employee)
            messages.success(request, 'Kullanıcı başarıyla kaydedildi! E-posta doğrulama bağlantısı gönderildi.')
            return redirect('aut_email_verify', slug=employee.slug)
        else:
            messages.error(request, f'{form.errors}  Formda hata var, lütfen kontrol edin.')

    else:
        form = CustomUserForm()

    return render(request, 'accounts/pages/employee_register.html', {'form': form})

def verify_email(request, slug):
    try:
        employee = Employee.objects.get(slug=slug)
        user = employee.user
        user.is_email_verified = True  # Kullanıcıyı doğrulama
        user.save()
        messages.success(request, 'E-posta başarıyla doğrulandı!')

        # E-posta doğrulandıktan sonra telefon doğrulama sayfasına yönlendirin
        return redirect('my_profile')  # Burada doğrulama kodunu talep etme sayfasının URL adını yazın

    except Employee.DoesNotExist:
        messages.error(request, 'Geçersiz doğrulama bağlantısı.')
        return redirect('my_profile')  # Ana sayfaya yönlendirme


def send_verification_email(employee):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from django.template.loader import render_to_string
    from django.utils.html import strip_tags

    # E-posta içeriği
    subject = 'E-posta Doğrulama'
    html_message = render_to_string('accounts/emails/verification_email.html', {'employee': employee})
    from_email = 'n.sekerci@agriknow.com.tr'  # Kendi e-posta adresinizi koyun
    to = employee.user.email

    # SMTP sunucusuna bağlan
    server = smtplib.SMTP('mail.kurumsaleposta.com', 587)
    server.starttls()  # TLS'yi başlat

    # Giriş yap
    server.login('info@agriknow.com.tr', 'PApatyam.3578')

    # Mesajı oluştur
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to
    msg['Subject'] = subject

    # Mesaj içeriği
    msg.attach(MIMEText(html_message, 'html', 'utf-8'))

    # E-postayı gönder
    server.send_message(msg)

    # Bağlantıyı kapat
    server.quit()





from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from company.models import CustomUser  # Kendi modelinizin yolu

def auth_password_reset_request (request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))  # force_bytes burada kullanılacak
            link = request.build_absolute_uri(reverse('auth_password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))

            send_password_reset_email(user.email, link)
            messages.success(request, 'E-posta adresinize şifre sıfırlama bağlantısı gönderildi.')
            return redirect('send_mail_reset_password')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Bu e-posta adresine kayıtlı bir kullanıcı bulunamadı.')

    return render(request, 'accounts/pages/password_reset_request.html')


def auth_password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                new_password1 = request.POST.get('new_password1')
                new_password2 = request.POST.get('new_password2')
                if new_password1 == new_password2: 
                    user.set_password(new_password1)
                    user.save()
                    messages.success(request, 'Şifreniz başarıyla değiştirildi. Giriş yapabilirsiniz.')
                    return redirect('auth_login')
                else:
                    messages.error(request, 'Şifreler eşleşmiyor.')
                    return redirect('auth_password_reset_confirm', uidb64=uidb64, token=token)
            return render(request, 'accounts/pages/password_reset_confirm.html', {'valid_link': True})

        messages.error(request, 'Geçersiz veya süresi dolmuş bağlantı.')
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        messages.error(request, 'Geçersiz bağlant.')

    return redirect('auth_password_reset_request')  # Şifre sıfırlama isteği sayfasına yönlendirme

def send_mail_reset_password(request):
    return render(request, 'accounts/pages/send_mail.html')

def send_password_reset_email(email, link):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from django.template.loader import render_to_string

    subject = 'Şifre Sıfırlama Talebi'
    html_message = render_to_string('accounts/emails/password_reset_email.html', {'link': link})
    from_email = 'n.sekerci@agriknow.com.tr'
    to = email

    try:
        # SMTP sunucusuna bağlan
        server = smtplib.SMTP('mail.kurumsaleposta.com', 587)
        server.starttls()  # TLS'yi başlat

        # Giriş yap
        server.login('info@agriknow.com.tr', 'PApatyam.3578')

        # Mesajı oluştur
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to
        msg['Subject'] = subject

        # Mesaj içeriği
        msg.attach(MIMEText(html_message, 'html', 'utf-8'))

        # E-postayı gönder
        server.send_message(msg)

    except Exception as e:
        print(f"E-posta gönderme hatası: {e}")
    finally:
        # Bağlantıyı kapat
        server.quit()


@login_required
def profile(request, slug=None):
    try:
        if slug:
            employee = Employee.objects.get(slug=slug)  # slug ile ilgili bir çalışanı bulmaya çalış
        else: 
            employee = Employee.objects.get(user=request.user)  # slug ile ilgili bir çalışanı bulmaya çalış
        context = {
            'title': 'Profile',
            'employee': employee
        }
        return render(request, 'main/pages/profile.html', context)
    except Employee.DoesNotExist:
        messages.error(request, 'Çalışan bulunamadı.')
        return redirect('auth_login')
    
import random
import requests
from django.contrib import messages
from django.shortcuts import render, redirect
from company.models import CustomUser  # Kendi modelinizin yolu

def send_verification_code(phone):
    url = "http://soap.netgsm.com.tr:8080/Sms_webservis/SMS?wsdl"
    headers = {'content-type': 'text/xml'}
    
    verification_code = random.randint(100000, 999999)

    try:
        user = CustomUser.objects.get(phone=phone)
    except CustomUser.DoesNotExist:
        # Kullanıcı bulunamazsa hata mesajı
        return None, "Bu telefon numarasıyla kayıtlı bir kullanıcı bulunamadı."

    mesaj = f"Sayın {user.first_name} {user.last_name}\n Telefon numaranızı doğrulamak için kodunuz: {verification_code}"
    body = f"""<?xml version="1.0"?>
        <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
                    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <SOAP-ENV:Body>
                <ns3:smsGonder1NV2 xmlns:ns3="http://sms/">
                    <username>8503081334</username>
                    <password>6D18AD8</password>
                    <header>MNC GROUP</header>
                    <msg>{mesaj}</msg>
                    <gsm>{phone}</gsm>
                    <encoding>TR</encoding>
                    <filter>0</filter>
                    <startdate></startdate>
                    <stopdate></stopdate>
                </ns3:smsGonder1NV2>
            </SOAP-ENV:Body>
        </SOAP-ENV:Envelope>"""
    
    response = requests.post(url, data=body, headers=headers)

    if response.status_code != 200:
        return None, "SMS gönderimi başarısız oldu."

    return verification_code

def auth_phone_verify(request, phone):
    masked_phone = f"*******{phone[-4:]}"
    if request.method == 'POST':
        code = request.POST.get('code')
        first = request.POST.get('first')
        second = request.POST.get('second')
        third = request.POST.get('third')
        fourth = request.POST.get('fourth')
        fifth = request.POST.get('fifth')
        sixth = request.POST.get('sixth')
        verification_code = f"{first}{second}{third}{fourth}{fifth}{sixth}"

        try:
            user = CustomUser.objects.get(phone=phone)
            # Oturumda saklanan kod ile kullanıcının girdiği kodu karşılaştır
            if code == verification_code:
                user.is_phone_verified = True
                user.save()
                messages.success(request, 'Telefon numaranız başarıyla doğrulandı!')
                return redirect('send_mail_reset_password')
            else:
                messages.error(request, 'Geçersiz doğrulama kodu.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Bu telefon numarasıyla kayıtlı bir kullanıcı bulunamadı.')
    else:
        verification_code = send_verification_code(phone)
        
    return render(request, 'accounts/pages/phone_verify.html', {'phone': phone, 'masked_phone': masked_phone, 'code': verification_code})

