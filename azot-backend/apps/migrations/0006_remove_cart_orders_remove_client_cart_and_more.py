# Generated by Django 5.0.6 on 2024-05-16 21:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0005_alter_seller_products_alter_seller_purchases'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='orders',
        ),
        migrations.RemoveField(
            model_name='client',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='seller',
            name='products',
        ),
        migrations.RemoveField(
            model_name='seller',
            name='purchases',
        ),
        migrations.AddField(
            model_name='client',
            name='client',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='apps.cart'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='cart',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='apps.cart'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchase',
            name='seller',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='apps.seller'),
            preserve_default=False,
        ),
    ]
