# Generated by Django 5.1.5 on 2025-01-26 01:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0003_booking'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='booking_date',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='is_confirmed',
        ),
    ]
