from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os

def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(max_length=1000, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to=get_image_path, null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class UserFriendShip(models.Model):
    from_user_id = models.IntegerField()
    to_user_id = models.IntegerField()
    is_accepted = models.BooleanField(default=False)
    is_pending = models.BooleanField(default=True)
    identifier = models.TextField()

