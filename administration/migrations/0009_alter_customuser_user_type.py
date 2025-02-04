# Generated by Django 5.1.4 on 2025-01-31 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0008_appointment_slug_alter_appointment_appointment_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(blank=True, choices=[('Patient', 'Patient'), ('Doctor', 'Doctor'), ('Staff', 'Staff')], default='', max_length=20, null=True),
        ),
    ]
