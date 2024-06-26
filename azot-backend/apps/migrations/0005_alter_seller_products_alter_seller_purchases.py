# Generated by Django 5.0.6 on 2024-05-16 21:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0004_alter_seller_products_alter_seller_purchases'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='products',
            field=models.ForeignKey(default={}, on_delete=django.db.models.deletion.CASCADE, to='apps.product'),
        ),
        migrations.AlterField(
            model_name='seller',
            name='purchases',
            field=models.ForeignKey(default={}, on_delete=django.db.models.deletion.CASCADE, to='apps.purchase'),
        ),
    ]
