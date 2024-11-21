# Generated by Django 5.0.6 on 2024-10-25 10:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('staff', 'Staff'), ('organizer', 'Organizer'), ('user', 'User')], default='user', max_length=10),
        ),
        migrations.AlterField(
            model_name='event',
            name='is_cancelled',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='organizer',
            field=models.ForeignKey(limit_choices_to={'role': 'organizer'}, on_delete=django.db.models.deletion.CASCADE, to='adminpanel.profile'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='id_proof',
            field=models.ImageField(blank=True, null=True, upload_to='id_proof/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='is_organizer',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_images/'),
        ),
    ]
