from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import News

@receiver(pre_delete, sender=User)
def assign_default_author(sender, instance, **kwargs):
    default_author = User.objects.get(username='default_admin')
    News.objects.filter(author=instance).update(author=default_author)