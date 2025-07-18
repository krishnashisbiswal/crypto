# Generated by Django 5.2.3 on 2025-07-10 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deposits', '0004_deposit_price_at_deposit_alter_deposit_coin_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deposit',
            name='price_at_deposit',
        ),
        migrations.AlterField(
            model_name='deposit',
            name='coin_quantity',
            field=models.DecimalField(decimal_places=10, default=0, max_digits=20),
        ),
    ]
