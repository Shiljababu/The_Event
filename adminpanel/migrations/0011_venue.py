# Generated by Django 5.0.6 on 2024-11-03 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0010_event_status_alter_event_event_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('map_link', models.URLField()),
                ('venue_image', models.ImageField(upload_to='venue_images/')),
            ],
        ),
    ]