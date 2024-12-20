# Generated by Django 5.1.2 on 2024-11-04 10:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0006_customuser_gender'),
        ('files', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='Created At'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='Is Active'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='updated_at',
            field=models.DateField(auto_now=True, verbose_name='Last Updated At'),
        ),
        migrations.AlterField(
            model_name='activitycost',
            name='activity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='files.activity', verbose_name='Activity'),
        ),
        migrations.AlterField(
            model_name='activitycost',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='Created At'),
        ),
        migrations.AlterField(
            model_name='activitycost',
            name='currency',
            field=models.CharField(choices=[('TL', 'TL'), ('USD', 'USD'), ('EUR', 'EUR'), ('RMB', 'RMB')], default='TL', max_length=3, verbose_name='Currency'),
        ),
        migrations.AlterField(
            model_name='activitycost',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='Is Active'),
        ),
        migrations.AlterField(
            model_name='activitycost',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='activitycost',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='files.activitysupplier', verbose_name='Activity Supplier'),
        ),
        migrations.AlterField(
            model_name='activitycost',
            name='updated_at',
            field=models.DateField(auto_now=True, verbose_name='Last Updated At'),
        ),
        migrations.AlterField(
            model_name='activitysupplier',
            name='contact',
            field=models.CharField(max_length=155, verbose_name='Contact'),
        ),
        migrations.AlterField(
            model_name='activitysupplier',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='Created At'),
        ),
        migrations.AlterField(
            model_name='activitysupplier',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='Is Active'),
        ),
        migrations.AlterField(
            model_name='activitysupplier',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='activitysupplier',
            name='updated_at',
            field=models.DateField(auto_now=True, verbose_name='Last Updated At'),
        ),
        migrations.AlterField(
            model_name='buyercompany',
            name='contact',
            field=models.CharField(blank=True, max_length=155, null=True, verbose_name='Contact'),
        ),
        migrations.AlterField(
            model_name='buyercompany',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='Created At'),
        ),
        migrations.AlterField(
            model_name='buyercompany',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='Is Active'),
        ),
        migrations.AlterField(
            model_name='buyercompany',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='buyercompany',
            name='short_name',
            field=models.CharField(max_length=5, unique=True, verbose_name='Short Name'),
        ),
        migrations.AlterField(
            model_name='buyercompany',
            name='updated_at',
            field=models.DateField(auto_now=True, verbose_name='Last Updated At'),
        ),
        migrations.AlterField(
            model_name='guide',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='Created At'),
        ),
        migrations.AlterField(
            model_name='guide',
            name='currency',
            field=models.CharField(choices=[('TL', 'TL'), ('USD', 'USD'), ('EUR', 'EUR'), ('RMB', 'RMB')], default='TL', max_length=3, verbose_name='Currency'),
        ),
        migrations.AlterField(
            model_name='guide',
            name='doc_no',
            field=models.CharField(blank=True, max_length=155, null=True, verbose_name='Guide No'),
        ),
        migrations.AlterField(
            model_name='guide',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='Is Active'),
        ),
        migrations.AlterField(
            model_name='guide',
            name='mail',
            field=models.CharField(blank=True, max_length=155, null=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='guide',
            name='name',
            field=models.CharField(max_length=155, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='guide',
            name='phone',
            field=models.CharField(max_length=155, verbose_name='Phone'),
        ),
        migrations.AlterField(
            model_name='guide',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='guide',
            name='updated_at',
            field=models.DateField(auto_now=True, verbose_name='Last Updated At'),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='Created At'),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='currency',
            field=models.CharField(choices=[('TL', 'TL'), ('USD', 'USD'), ('EUR', 'EUR'), ('RMB', 'RMB')], default='TL', max_length=3, verbose_name='Currency'),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='finish',
            field=models.DateField(blank=True, null=True, verbose_name='Price Geçerlilik Tarihi'),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='Is Active'),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='mail',
            field=models.CharField(blank=True, max_length=155, null=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='one_person',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Tek Kişilik Price'),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='tree_person',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Üç Kişilik Price'),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='two_person',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='İki Kişilik Price'),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='updated_at',
            field=models.DateField(auto_now=True, verbose_name='Last Updated At'),
        ),
        migrations.AlterField(
            model_name='museum',
            name='contact',
            field=models.CharField(blank=True, max_length=155, null=True, verbose_name='Contact'),
        ),
        migrations.AlterField(
            model_name='museum',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='Created At'),
        ),
        migrations.AlterField(
            model_name='museum',
            name='currency',
            field=models.CharField(choices=[('TL', 'TL'), ('USD', 'USD'), ('EUR', 'EUR'), ('RMB', 'RMB')], default='TL', max_length=3, verbose_name='Currency'),
        ),
        migrations.AlterField(
            model_name='museum',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='Is Active'),
        ),
        migrations.AlterField(
            model_name='museum',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='museum',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='museum',
            name='updated_at',
            field=models.DateField(auto_now=True, verbose_name='Last Updated At'),
        ),
        migrations.AlterField(
            model_name='novehicletour',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='Created At'),
        ),
        migrations.AlterField(
            model_name='novehicletour',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='Is Active'),
        ),
        migrations.AlterField(
            model_name='novehicletour',
            name='route',
            field=models.CharField(max_length=155, verbose_name='Route'),
        ),
        migrations.AlterField(
            model_name='novehicletour',
            name='updated_at',
            field=models.DateField(auto_now=True, verbose_name='Last Updated At'),
        ),
        migrations.AlterField(
            model_name='tour',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='Created At'),
        ),
        migrations.AlterField(
            model_name='tour',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='Is Active'),
        ),
        migrations.AlterField(
            model_name='tour',
            name='route',
            field=models.CharField(max_length=155, verbose_name='Route'),
        ),
        migrations.AlterField(
            model_name='tour',
            name='updated_at',
            field=models.DateField(auto_now=True, verbose_name='Last Updated At'),
        ),
        migrations.AlterField(
            model_name='transfer',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='Created At'),
        ),
        migrations.AlterField(
            model_name='transfer',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='Is Active'),
        ),
        migrations.AlterField(
            model_name='transfer',
            name='route',
            field=models.CharField(max_length=155, verbose_name='Route'),
        ),
        migrations.AlterField(
            model_name='transfer',
            name='updated_at',
            field=models.DateField(auto_now=True, verbose_name='Last Updated At'),
        ),
        migrations.AlterField(
            model_name='useractivitylog',
            name='browser_info',
            field=models.TextField(blank=True, null=True, verbose_name='Tarayıcı Info'),
        ),
        migrations.AlterField(
            model_name='useractivitylog',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='Created At'),
        ),
        migrations.AlterField(
            model_name='useractivitylog',
            name='ip_address',
            field=models.GenericIPAddressField(blank=True, null=True, verbose_name='IP Address'),
        ),
        migrations.AlterField(
            model_name='useractivitylog',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='Is Active'),
        ),
        migrations.AlterField(
            model_name='useractivitylog',
            name='staff',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.employee', verbose_name='Employee'),
        ),
        migrations.AlterField(
            model_name='useractivitylog',
            name='updated_at',
            field=models.DateField(auto_now=True, verbose_name='Last Updated At'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='capacity',
            field=models.PositiveIntegerField(verbose_name='Capacity'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='Created At'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='Is Active'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='updated_at',
            field=models.DateField(auto_now=True, verbose_name='Last Updated At'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='vehicle',
            field=models.CharField(max_length=155, verbose_name='Vehicle'),
        ),
        migrations.AlterField(
            model_name='vehiclecost',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='Created At'),
        ),
        migrations.AlterField(
            model_name='vehiclecost',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='Is Active'),
        ),
        migrations.AlterField(
            model_name='vehiclecost',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='files.vehiclesupplier', verbose_name='Supplier'),
        ),
        migrations.AlterField(
            model_name='vehiclecost',
            name='updated_at',
            field=models.DateField(auto_now=True, verbose_name='Last Updated At'),
        ),
        migrations.AlterField(
            model_name='vehiclecostprice',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='Created At'),
        ),
        migrations.AlterField(
            model_name='vehiclecostprice',
            name='currency',
            field=models.CharField(choices=[('TL', 'TL'), ('USD', 'USD'), ('EUR', 'EUR'), ('RMB', 'RMB')], default='TL', max_length=3, verbose_name='Currency'),
        ),
        migrations.AlterField(
            model_name='vehiclecostprice',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='Is Active'),
        ),
        migrations.AlterField(
            model_name='vehiclecostprice',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='vehiclecostprice',
            name='updated_at',
            field=models.DateField(auto_now=True, verbose_name='Last Updated At'),
        ),
        migrations.AlterField(
            model_name='vehiclecostprice',
            name='vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='files.vehicle', verbose_name='Vehicle'),
        ),
        migrations.AlterField(
            model_name='vehiclesupplier',
            name='contact',
            field=models.CharField(max_length=155, verbose_name='Contact'),
        ),
        migrations.AlterField(
            model_name='vehiclesupplier',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='Created At'),
        ),
        migrations.AlterField(
            model_name='vehiclesupplier',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='Is Active'),
        ),
        migrations.AlterField(
            model_name='vehiclesupplier',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='vehiclesupplier',
            name='updated_at',
            field=models.DateField(auto_now=True, verbose_name='Last Updated At'),
        ),
    ]
