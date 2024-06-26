# Generated by Django 5.0.6 on 2024-05-10 21:06

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.UUIDField(default=uuid.UUID('a3094730-1511-4c1c-9f2f-646dba7d944f'), editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.UUIDField(default=uuid.UUID('170e9ee1-c26a-40e2-ad0f-3a223c87bf86'), editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.UUID('605c84b2-d464-4674-9f82-9fabb0b28694'), editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('image', models.URLField()),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.seller')),
            ],
        ),
    ]
