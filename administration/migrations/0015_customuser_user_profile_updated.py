# Generated by Django 5.1.4 on 2025-02-09 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0014_patient_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_profile_updated',
            field=models.BooleanField(default=False),
        ),
    ]
