# Generated by Django 5.1.4 on 2025-01-24 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0010_rename_employee_code_doctor_employ_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='pat_mrd_no',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
