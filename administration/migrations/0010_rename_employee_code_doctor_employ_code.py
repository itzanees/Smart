# Generated by Django 5.1.4 on 2025-01-23 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0009_customuser_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doctor',
            old_name='employee_code',
            new_name='employ_code',
        ),
    ]
