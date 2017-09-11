import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

from .utils import unique_slug_generator
from .validators import validate_location, validate_title


# Create your models here.
@python_2_unicode_compatible
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, validators=[validate_title])
    contents = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=120, null=True, blank=True, validators=[validate_location])
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.title

    def was_published_recently(self):
        return self.timestamp >= timezone.now() - datetime.timedelta(days=1)


# Instance saving signals below
def rl_pre_save_reciever(sender, instance, *args, **kwargs):
    instance.location = instance.location.capitalize()
    print('saving..')
    print(instance.timestamp)
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

def rl_post_save_reciever(sender, instance, created, *args, **kwargs):
    print('saved')
    print(instance.timestamp)

pre_save.connect(rl_pre_save_reciever, sender=Post)
post_save.connect(rl_post_save_reciever, sender=Post)
