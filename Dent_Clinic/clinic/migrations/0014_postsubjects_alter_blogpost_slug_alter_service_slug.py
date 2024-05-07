# Generated by Django 5.0.4 on 2024-05-07 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0013_review_service_alter_appointment_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostSubjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=40, verbose_name='Тематика')),
            ],
            options={
                'verbose_name': 'Тематика поста',
                'verbose_name_plural': 'Тематики постов',
            },
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='slug',
            field=models.SlugField(max_length=300, unique_for_date='created', verbose_name='Слаг (заполняется автоматически)'),
        ),
        migrations.AlterField(
            model_name='service',
            name='slug',
            field=models.SlugField(max_length=300, verbose_name='Слаг (заполняется автоматически)'),
        ),
    ]
