# Generated by Django 5.0.6 on 2024-05-16 21:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0003_cart_rename_seller_product_owner_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='products',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='apps.product'),
        ),
        migrations.AlterField(
            model_name='seller',
            name='purchases',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='apps.purchase'),
        ),
    ]