# Generated by Django 4.1 on 2023-03-07 06:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0011_alter_post_text_body_alter_post_text_body_en_us_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='text_body_en_us',
        ),
        migrations.RemoveField(
            model_name='post',
            name='text_body_ru',
        ),
        migrations.RemoveField(
            model_name='post',
            name='title_en_us',
        ),
        migrations.RemoveField(
            model_name='post',
            name='title_ru',
        ),
    ]
