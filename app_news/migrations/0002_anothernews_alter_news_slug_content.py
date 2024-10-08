# Generated by Django 5.1.1 on 2024-09-07 16:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_news', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnotherNews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('slug', models.SlugField(max_length=150)),
                ('created_time', models.TimeField(auto_now_add=True)),
                ('update_time', models.TimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='news',
            name='slug',
            field=models.SlugField(max_length=200),
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_type', models.CharField(choices=[('text', 'Text'), ('imeage', 'Image'), ('video', 'Video')], max_length=10)),
                ('text', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='news_images/')),
                ('video_link', models.URLField(blank=True, null=True)),
                ('order', models.IntegerField(default=0)),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contents', to='app_news.anothernews')),
            ],
        ),
    ]
