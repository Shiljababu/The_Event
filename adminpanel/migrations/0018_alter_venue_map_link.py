# Generated by Django 5.0.6 on 2024-11-04 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0017_alter_venue_map_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='map_link',
            field=models.URLField(max_length=500),
        ),
    ]
