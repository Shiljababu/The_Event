# Generated by Django 5.0.6 on 2024-11-07 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0021_delete_castorteamimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(choices=[('movie', 'Movie'), ('event', 'Event'), ('play', 'Play'), ('activity', 'Activity'), ('sport', 'Sport')], default='event', max_length=20),
        ),
    ]
