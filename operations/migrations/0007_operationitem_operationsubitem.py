# Generated by Django 5.1.2 on 2024-11-13 18:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0006_remove_operationsubitem_content_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OperationItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_type', models.CharField(max_length=50)),
                ('attributes', models.JSONField(blank=True, null=True)),
                ('order', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('operation_day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operation_items', to='operations.operationday')),
            ],
        ),
        migrations.CreateModel(
            name='OperationSubItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_item_type', models.CharField(max_length=50)),
                ('attributes', models.JSONField(blank=True, null=True)),
                ('order', models.PositiveIntegerField()),
                ('operation_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_items', to='operations.operationitem')),
            ],
        ),
    ]
