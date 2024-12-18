# Generated by Django 5.0.6 on 2024-11-09 05:07

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0025_ticket_ticket_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='quantity_available_premium',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='quantity_available_standard',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='quantity_sold_premium',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='quantity_sold_standard',
        ),
        migrations.AddField(
            model_name='event',
            name='quantity_sold_premium',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='event',
            name='quantity_sold_standard',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='event',
            name='seats_available_premium',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='event',
            name='seats_available_standard',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='ticket',
            name='booking_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ticket',
            name='quantity_booked',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
