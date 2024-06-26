# Generated by Django 5.0.4 on 2024-05-07 10:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0014_postsubjects_alter_blogpost_slug_alter_service_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postsubjects',
            old_name='subject',
            new_name='post_subject',
        ),
        migrations.AddField(
            model_name='blogpost',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subject', to='clinic.postsubjects'),
        ),
    ]
