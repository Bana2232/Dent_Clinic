# Generated by Django 5.0.4 on 2024-04-20 17:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0008_alter_appointment_target'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='target',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='service_appointments', to='clinic.service'),
        ),
    ]
