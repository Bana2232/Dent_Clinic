# Generated by Django 5.0.4 on 2024-04-13 07:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0002_doctor_works_from'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doctor',
            old_name='works_from',
            new_name='works_since',
        ),
    ]
