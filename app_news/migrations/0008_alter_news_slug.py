# Generated by Django 5.1.1 on 2024-09-09 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_news', '0007_alter_news_managers_alter_news_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='slug',
            field=models.SlugField(max_length=200, unique=True),
        ),
    ]
