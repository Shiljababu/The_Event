# Generated by Django 5.0.6 on 2024-11-21 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0054_alter_interest_unique_together'),
    ]

    operations = [
        migrations.RenameField(
            model_name='interest',
            old_name='interested_at',
            new_name='created_at',
        ),
    ]
