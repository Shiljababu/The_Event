# Generated by Django 5.0.6 on 2024-11-04 03:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0015_remove_event_cast_or_team_event_cast_or_team_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='cast_or_team_image',
        ),
        migrations.RemoveField(
            model_name='event',
            name='event_schedule',
        ),
        migrations.CreateModel(
            name='CastOrTeamImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='cast_or_team/')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cast_or_team_images', to='adminpanel.event')),
            ],
        ),
    ]
