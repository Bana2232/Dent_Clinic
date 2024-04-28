# Generated by Django 5.0.4 on 2024-04-24 06:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0010_alter_serviceimages_image_alter_user_address_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appointment',
            options={'verbose_name': 'Запись', 'verbose_name_plural': 'Записи'},
        ),
        migrations.AlterModelOptions(
            name='blogpost',
            options={'ordering': ['-publish'], 'verbose_name': 'Пост', 'verbose_name_plural': 'Посты'},
        ),
        migrations.AlterModelOptions(
            name='doctor',
            options={'verbose_name': 'Врач', 'verbose_name_plural': 'Врачи'},
        ),
        migrations.AlterModelOptions(
            name='doctorimages',
            options={'verbose_name': 'Фотография врача', 'verbose_name_plural': 'Фотографии врачей'},
        ),
        migrations.AlterModelOptions(
            name='postimages',
            options={'verbose_name': 'Изображение поста', 'verbose_name_plural': 'Изображения постов'},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'verbose_name': 'Отзыв', 'verbose_name_plural': 'Отзывы'},
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'verbose_name': 'Услуга', 'verbose_name_plural': 'Услуги'},
        ),
        migrations.AlterModelOptions(
            name='serviceimages',
            options={'verbose_name': 'Изображение услуги', 'verbose_name_plural': 'Изображения услуг'},
        ),
        migrations.AlterModelOptions(
            name='servicevideo',
            options={'verbose_name': 'Видео услуги', 'verbose_name_plural': 'Видео услуг'},
        ),
    ]
