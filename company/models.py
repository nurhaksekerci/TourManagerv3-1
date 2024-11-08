from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    phone = models.CharField(max_length=15, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="F")  # Gender field added here
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    last_password_change = models.DateTimeField(null=True, blank=True)
    two_factor_enabled = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)

    def __str__(self):
        return self.email


class City(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='City Name')
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            name_with_i = self.name.replace('ı', 'i')
            self.slug = slugify(name_with_i)

            # Benzersiz slug kontrolü
            original_slug = self.slug
            counter = 1
            while City.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Cities"
        ordering = ['name']


class District(models.Model):
    name = models.CharField(max_length=100, verbose_name='District Name')
    city = models.ForeignKey(City, related_name='districts', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            district_name_with_i = self.name.replace('ı', 'i')
            city_name_with_i = self.city.name.replace('ı', 'i')
            self.slug = slugify(f"{district_name_with_i}-{city_name_with_i}")

            # Benzersiz slug kontrolü
            original_slug = self.slug
            counter = 1
            while District.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
            
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}, {self.city.name}"

    class Meta:
        ordering = ['name']


class Neighborhood(models.Model):
    name = models.CharField(max_length=100, verbose_name='Neighborhood Name')
    district = models.ForeignKey(District, related_name='neighborhoods', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            neighborhood_name_with_i = self.name.replace('ı', 'i')
            district_name_with_i = self.district.name.replace('ı', 'i')
            self.slug = slugify(f"{neighborhood_name_with_i}-{district_name_with_i}")

            # Benzersiz slug kontrolü
            original_slug = self.slug
            counter = 1
            while Neighborhood.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
            
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}, {self.district.name}"

    class Meta:
        ordering = ['name']


class SalesAgent(models.Model):
    name = models.CharField(verbose_name=("Name"), max_length=126)
    city = models.ForeignKey(City, verbose_name=("City"), related_name='sales_agents', on_delete=models.CASCADE)
    district = models.ForeignKey(District, verbose_name=("District"), related_name='sales_agents', on_delete=models.CASCADE)
    neighborhood = models.ForeignKey(Neighborhood, verbose_name=("Neighborhood"), related_name='sales_agents', on_delete=models.CASCADE)
    address = models.TextField(verbose_name=("Address"))
    slug = models.SlugField(unique=True, blank=True)
    number_of_sales = models.PositiveIntegerField(verbose_name=("Number of Sales"), default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            agent_name_with_i = self.name.replace('ı', 'i')
            neighborhood_name_with_i = self.neighborhood.name.replace('ı', 'i')
            district_name_with_i = self.district.name.replace('ı', 'i')
            city_name_with_i = self.city.name.replace('ı', 'i')
            self.slug = slugify(f"{agent_name_with_i}-{neighborhood_name_with_i}-{district_name_with_i}-{city_name_with_i}")

            # Benzersiz slug kontrolü
            original_slug = self.slug
            counter = 1
            while SalesAgent.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}, {self.neighborhood.name}, {self.district.name}, {self.city.name}"


class SalesAgentDoc(models.Model):
    sales_agent = models.ForeignKey(SalesAgent, verbose_name=("Sales Agent"), related_name='documents', on_delete=models.CASCADE)
    doc_name = models.CharField(verbose_name=("Doc Name"), max_length=255)
    file = models.FileField(verbose_name=("File"), upload_to="agents/", max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.doc_name} (Agent: {self.sales_agent.name})"


class SalesAgentUser(models.Model):
    sales_agent = models.ForeignKey(SalesAgent, verbose_name=("Sales Agent"), related_name='users', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, verbose_name=("User"), related_name='sales_agent_users', on_delete=models.CASCADE)
    phone = models.CharField(verbose_name=("Phone"), max_length=50)
    is_manager = models.BooleanField(default=False)
    terms_read = models.BooleanField(default=False)
    kvkk_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} (Agent: {self.sales_agent.name})"


class Company(models.Model):
    name = models.CharField(verbose_name=("Name"), max_length=126)
    city = models.ForeignKey(City, verbose_name=("City"), related_name='companies', on_delete=models.CASCADE)
    district = models.ForeignKey(District, verbose_name=("District"), related_name='companies', on_delete=models.CASCADE)
    neighborhood = models.ForeignKey(Neighborhood, verbose_name=("Neighborhood"), related_name='companies', on_delete=models.CASCADE)
    address = models.TextField(verbose_name=("Address"))
    complete_at = models.DateField(verbose_name=("Complete Date"), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    branch = models.PositiveIntegerField(verbose_name=("Branch"), default=0)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            name_with_i = self.name.replace('ı', 'i')
            self.slug = slugify(name_with_i)

            # Benzersiz slug kontrolü
            original_slug = self.slug
            counter = 1

            while Company.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}, {self.neighborhood.name}, {self.district.name}, {self.city.name}"



class SalesAgentCustomer(models.Model):
    sales_agent = models.ForeignKey(SalesAgent, verbose_name=("Sales Agent"), related_name='customers', on_delete=models.CASCADE)
    company = models.ForeignKey(Company, verbose_name=("Company"), related_name='sales_agent_customers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sales_agent.name} - {self.company.name}"


class CompanyDoc(models.Model):
    company = models.ForeignKey(Company, verbose_name=("Company"), related_name='documents', on_delete=models.CASCADE)
    doc_name = models.CharField(verbose_name=("Doc Name"), max_length=255)
    file = models.FileField(verbose_name=("File"), upload_to="companies/", max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.doc_name} (Company: {self.company.name})"

class Branch(models.Model):
    company = models.ForeignKey(Company, verbose_name=("Company"), related_name='branches', on_delete=models.CASCADE)
    name = models.CharField(verbose_name=("Name"), max_length=126)
    city = models.ForeignKey(City, verbose_name=("City"), related_name='branches', on_delete=models.CASCADE)
    district = models.ForeignKey(District, verbose_name=("District"), related_name='branches', on_delete=models.CASCADE)
    neighborhood = models.ForeignKey(Neighborhood, verbose_name=("Neighborhood"), related_name='branches', on_delete=models.CASCADE)
    address = models.TextField(verbose_name=("Address"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        # Slug oluştur
        if not self.slug:
            name_with_i = self.name.replace('ı', 'i')
            company_name_with_i = self.company.name.replace('ı', 'i')
            self.slug = slugify(f"{company_name_with_i}-{name_with_i}")

        # Benzersiz slug kontrolü
            original_slug = self.slug
            counter = 1

            while Branch.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.company.name}"

class Employee(models.Model):
    branch = models.ForeignKey(Branch, verbose_name=("Branch"), related_name='employees', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, verbose_name=("User"), related_name='employees', on_delete=models.CASCADE)
    is_manager = models.BooleanField(default=False)
    terms_read = models.BooleanField(default=True)
    kvkk_read = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        # Slug oluştur
        if not self.slug:
            branch_name_with_i = self.branch.company.name.replace('ı', 'i')
            self.slug = slugify(f"{branch_name_with_i}-{self.user.username}")

            # Benzersiz slug kontrolü
            original_slug = self.slug
            counter = 1

            while Employee.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} (Branch: {self.branch.name})"

