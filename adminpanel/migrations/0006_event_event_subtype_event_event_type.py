# Generated by Django 5.0.6 on 2024-10-27 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0005_event_event_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_subtype',
            field=models.CharField(blank=True, choices=[('action', 'Action Movie'), ('drama', 'Drama Movie'), ('comedy_movie', 'Comedy Movie'), ('musical_show', 'Musical Show'), ('comedy_show', 'Comedy Show'), ('conference', 'Conference'), ('meetup', 'Meetup'), ('soccer', 'Soccer'), ('basketball', 'Basketball'), ('tennis', 'Tennis'), ('theater', 'Theater Play'), ('drama_play', 'Drama Play'), ('musical_play', 'Musical Play'), ('workshop', 'Workshop'), ('outdoor_activity', 'Outdoor Activity'), ('indoor_activity', 'Indoor Activity')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='event_type',
            field=models.CharField(choices=[('movie', 'Movie'), ('musical_show', 'Musical Show'), ('play', 'Play'), ('activity', 'Activity'), ('sport', 'Sport')], default='event', max_length=20),
        ),
    ]
