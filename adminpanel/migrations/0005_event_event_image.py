# Generated by Django 5.0.6 on 2024-10-27 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0004_remove_profile_organizer_alter_profile_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_image',
            field=models.ImageField(blank=True, null=True, upload_to='event_image/'),
        ),
    ]
