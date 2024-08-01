import string
import random
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Quest(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    exp = models.IntegerField()

    def __str__(self):
        return self.title

class HoinkyUser(AbstractUser):
    quests_achieved = models.ManyToManyField(Quest, blank=True)
    level = models.IntegerField(default=1)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    qr_unique = models.CharField(max_length=6, unique=True, blank=True)

    def __str__(self):
        return self.username

def generate_random_string(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@receiver(pre_save, sender=HoinkyUser)
def add_unique_qr_code(sender, instance, **kwargs):
    if not instance.qr_unique:
        instance.qr_unique = generate_random_string()
