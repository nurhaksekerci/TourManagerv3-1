from django.db import models
from company.models import CustomUser

# Create your models here.
class Egitmen(models.Model):
    name = models.CharField(verbose_name=("Name"), max_length=50)
    phone = models.CharField(verbose_name=("Phone"), max_length=50)
    photo = models.FileField(verbose_name=("Photo"), upload_to="egitmen/", max_length=255)

    def __str__(self):
        return self.name

class EgitimPlan(models.Model):
    # Gün seçim seçenekleri
    DAY_CHOICES = [
        ('13', '13'),
        ('14', '14'),
        ('15', '15'),
        ('18', '18'),
        ('19', '19'),
        ('20', '20'),
    ]

    name = models.CharField(verbose_name=("Name"), max_length=50)
    phone = models.CharField(verbose_name=("Phone"), max_length=50)
    egitmen = models.ForeignKey('Egitmen', verbose_name=("Teacher"), on_delete=models.CASCADE)
    day = models.CharField(max_length=2, choices=DAY_CHOICES, verbose_name="Training Time")

    def __str__(self):
        return str(self.name)
