# Generated by Django 5.0.6 on 2024-11-07 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0022_alter_event_event_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankaccount',
            name='account_number',
            field=models.CharField(default='account_0001', max_length=12, unique=True),
        ),
        migrations.AddField(
            model_name='bankaccount',
            name='currency',
            field=models.CharField(default='USD', max_length=3),
        ),
        migrations.AddField(
            model_name='bankaccount',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('suspended', 'Suspended'), ('closed', 'Closed')], default='active', max_length=20),
        ),
    ]
