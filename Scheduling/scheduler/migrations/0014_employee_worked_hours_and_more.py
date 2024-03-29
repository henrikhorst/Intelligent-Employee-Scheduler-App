# Generated by Django 4.1.7 on 2023-05-19 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0013_remove_preferences_my_field_preferences_friday_1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='worked_hours',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='employee',
            name='working_hours_per_week',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
