# Generated by Django 5.2.3 on 2025-07-10 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deposits', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deposit',
            name='price_at_deposit',
            field=models.DecimalField(decimal_places=8, default=0, max_digits=20),
        ),
    ]
