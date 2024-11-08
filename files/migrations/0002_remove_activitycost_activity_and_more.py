# Generated by Django 5.1.2 on 2024-11-01 12:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activitycost',
            name='activity',
        ),
        migrations.RemoveField(
            model_name='activitycost',
            name='company',
        ),
        migrations.RemoveField(
            model_name='activitycost',
            name='supplier',
        ),
        migrations.RemoveField(
            model_name='activitysupplier',
            name='company',
        ),
        migrations.RemoveField(
            model_name='activitysupplier',
            name='location',
        ),
        migrations.RemoveField(
            model_name='buyercompany',
            name='company',
        ),
        migrations.RemoveField(
            model_name='guide',
            name='company',
        ),
        migrations.RemoveField(
            model_name='guide',
            name='location',
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='company',
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='location',
        ),
        migrations.RemoveField(
            model_name='museum',
            name='company',
        ),
        migrations.RemoveField(
            model_name='museum',
            name='location',
        ),
        migrations.RemoveField(
            model_name='novehicletour',
            name='city',
        ),
        migrations.RemoveField(
            model_name='novehicletour',
            name='company',
        ),
        migrations.RemoveField(
            model_name='tour',
            name='company',
        ),
        migrations.RemoveField(
            model_name='tour',
            name='finish_city',
        ),
        migrations.RemoveField(
            model_name='tour',
            name='start_city',
        ),
        migrations.RemoveField(
            model_name='vehiclecost',
            name='tour',
        ),
        migrations.RemoveField(
            model_name='transfer',
            name='company',
        ),
        migrations.RemoveField(
            model_name='transfer',
            name='finish_city',
        ),
        migrations.RemoveField(
            model_name='transfer',
            name='start_city',
        ),
        migrations.RemoveField(
            model_name='vehiclecost',
            name='transfer',
        ),
        migrations.RemoveField(
            model_name='useractivitylog',
            name='company',
        ),
        migrations.RemoveField(
            model_name='useractivitylog',
            name='staff',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='company',
        ),
        migrations.RemoveField(
            model_name='vehiclecostprice',
            name='vehicle',
        ),
        migrations.RemoveField(
            model_name='vehiclecost',
            name='company',
        ),
        migrations.RemoveField(
            model_name='vehiclecost',
            name='supplier',
        ),
        migrations.RemoveField(
            model_name='vehiclecostprice',
            name='vehicle_cost',
        ),
        migrations.RemoveField(
            model_name='vehiclesupplier',
            name='company',
        ),
        migrations.RemoveField(
            model_name='vehiclesupplier',
            name='location',
        ),
        migrations.DeleteModel(
            name='Activity',
        ),
        migrations.DeleteModel(
            name='Activitycost',
        ),
        migrations.DeleteModel(
            name='Activitysupplier',
        ),
        migrations.DeleteModel(
            name='Buyercompany',
        ),
        migrations.DeleteModel(
            name='Guide',
        ),
        migrations.DeleteModel(
            name='Hotel',
        ),
        migrations.DeleteModel(
            name='Museum',
        ),
        migrations.DeleteModel(
            name='NoVehicleTour',
        ),
        migrations.DeleteModel(
            name='Tour',
        ),
        migrations.DeleteModel(
            name='Transfer',
        ),
        migrations.DeleteModel(
            name='UserActivityLog',
        ),
        migrations.DeleteModel(
            name='Vehicle',
        ),
        migrations.DeleteModel(
            name='Vehiclecost',
        ),
        migrations.DeleteModel(
            name='VehicleCostPrice',
        ),
        migrations.DeleteModel(
            name='VehicleSupplier',
        ),
    ]
