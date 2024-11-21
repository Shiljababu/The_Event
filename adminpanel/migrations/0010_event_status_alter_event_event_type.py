# Generated by Django 5.0.6 on 2024-10-27 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0009_alter_event_event_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='status',
            field=models.CharField(default='visible', max_length=20),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(choices=[('movie', 'Movie'), ('events', 'Events'), ('play', 'Play'), ('activities', 'Activities'), ('sports', 'Sports')], default='event', max_length=20),
        ),
    ]