# Generated by Django 4.1 on 2023-03-07 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0010_post_text_body_en_us_post_text_body_ru_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='text_body',
            field=models.TextField(default='NULL'),
        ),
        migrations.AlterField(
            model_name='post',
            name='text_body_en_us',
            field=models.TextField(default='NULL', null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='text_body_ru',
            field=models.TextField(default='NULL', null=True),
        ),
    ]
