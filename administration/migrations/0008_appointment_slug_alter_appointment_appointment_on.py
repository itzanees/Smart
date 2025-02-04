# Generated by Django 5.1.4 on 2025-01-28 23:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0007_alter_appointment_appointment_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='slug',
            field=models.SlugField(default='', max_length=32),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='appointment_on',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='schedule', to='administration.schedule'),
        ),
    ]
