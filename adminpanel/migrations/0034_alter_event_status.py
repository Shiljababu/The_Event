# Generated by Django 5.0.6 on 2024-11-11 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0033_alter_event_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='status',
            field=models.CharField(default='visible', max_length=20),
        ),
    ]
