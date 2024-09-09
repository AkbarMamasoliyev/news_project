from django.utils import timezone
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


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

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("single_page", args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)



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
    message = models.TextField

    class Meta:
        verbose_name_plural = 'Contact'

    def __str__(self):
        return self.email
