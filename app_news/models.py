from django.utils import timezone
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class PublishedManager(models.Manager):
    def published(self):
        return super().get_queryset().filter(status='PB')


class News(models.Model):

    class Status(models.TextChoices):
        Draft = 'DF', 'draft'
        Published = 'PB', 'published'

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    body = models.TextField()
    image = models.ImageField(upload_to='news/images')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    published_time = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey('app_news.Categories', on_delete=models.CASCADE)
    status = models.CharField(max_length=2,
                               choices=Status.choices,
                               default=Status.Draft
                               )
    author = models.ForeignKey('app_news.Authors', null=True, blank=True, on_delete=models.SET_NULL)

    published = PublishedManager()
    objects = models.Manager()

    class Meta:
        ordering = ['-published_time']
        verbose_name_plural = 'News'
        verbose_name = 'one news'

    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Categories(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Categories'
        verbose_name = 'category'

    def save(self, *args, **kwargs):
        if self.name == "o'zbekiston":
            self.slug = 'uzbekiston'
        elif not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Authors(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Authors'
        verbose_name = 'author'

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=150)
    message = models.TextField(null=True)

    class Meta:
        verbose_name_plural = 'Contact'

    def __str__(self):
        return self.email


class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE,
                             related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='comments')
    body = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)


    class Meta:
        ordering = ['created_time']

    def __str__(self):
        return f"Comment -  {self.body} by {self.user}"

