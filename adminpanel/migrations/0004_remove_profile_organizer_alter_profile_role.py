# Generated by Django 5.0.6 on 2024-10-25 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0003_rename_is_organizer_profile_organizer_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='organizer',
        ),
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('organizer', 'Organizer'), ('user', 'User')], default='user', max_length=10),
        ),
    ]
