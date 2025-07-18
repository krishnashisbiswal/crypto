# Generated by Django 5.2.3 on 2025-07-10 11:05

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deposits', '0005_remove_deposit_price_at_deposit_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deposit',
            name='coin_quantity',
            field=models.DecimalField(decimal_places=10, default=Decimal('0'), max_digits=30),
        ),
    ]
