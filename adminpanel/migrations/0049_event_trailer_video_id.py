# Generated by Django 5.0.6 on 2024-11-18 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0048_reviewlikedislike'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='trailer_video_id',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
