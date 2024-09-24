from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,)
    user_profile_photo = models.ImageField(upload_to='users/', blank=True, null=True)
    date_of_birthday = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Profiles'
        verbose_name = 'profile'
    def __str__(self):
        return self.user.username
