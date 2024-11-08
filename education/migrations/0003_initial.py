# Generated by Django 5.1.2 on 2024-11-08 17:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('education', '0002_remove_egitimplan_egitmen_remove_egitimplan_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Egitmen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('phone', models.CharField(max_length=50, verbose_name='Phone')),
                ('photo', models.FileField(max_length=255, upload_to='egitmen/', verbose_name='Photo')),
            ],
        ),
        migrations.CreateModel(
            name='EgitimPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('phone', models.CharField(max_length=50, verbose_name='Phone')),
                ('day', models.CharField(choices=[('13', '13'), ('14', '14'), ('15', '15'), ('18', '18'), ('19', '19'), ('20', '20')], max_length=2, verbose_name='Training Time')),
                ('egitmen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.egitmen', verbose_name='Teacher')),
            ],
        ),
    ]