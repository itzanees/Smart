# Generated by Django 5.1.4 on 2025-02-18 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0034_remove_medicalrecord_department_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone_num', models.CharField(max_length=10)),
                ('contact_type', models.CharField(choices=[('ME', 'Message'), ('EQ', 'Enquiry'), ('SU', 'Suggestion'), ('CO', 'Complaint')], max_length=2)),
                ('message', models.TextField()),
            ],
        ),
    ]
