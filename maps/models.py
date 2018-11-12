import datetime
import re

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from separatedvaluesfield.models import SeparatedValuesField
from django.db.models.signals import post_save, pre_save
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

from .utils import unique_slug_generator, grab_location
from .validators import validate_location, validate_title, validate_username

from django.contrib.auth.models import User
from django.dispatch import receiver

        
# Customized user models here.
class Profile(models.Model):

    def __str__(self):
        return str(self.user)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    watchlist = SeparatedValuesField(
    null=True,
    max_length=500,
    token=',',
    )

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



User = settings.AUTH_USER_MODEL

# Create your models here.
@python_2_unicode_compatible
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, validators=[validate_username])
    title = models.CharField(max_length=200, validators=[validate_title])
    contents = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=120, null=True, blank=True, validators=[validate_location])
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'slug': self.slug})

    def was_published_recently(self):
        return self.timestamp >= timezone.now() - datetime.timedelta(days=1)

    def get_contents_preview(self):
        if len(self.contents) < 200:
            return self.contents
        else:
            regex = r"^((?:\S+\s+){25}\S+)"
            match = re.findall(regex, self.contents)
            short_contents = "{}...".format(match[0])
            return short_contents


# Instance saving signals below
def rl_pre_save_reciever(sender, instance, *args, **kwargs):
    print('saving..')
    print(instance.timestamp)
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

    if not instance.location:
        instance.location = grab_location(instance)

def rl_post_save_reciever(sender, instance, created, *args, **kwargs):
    print('saved')
    print(instance.timestamp)

pre_save.connect(rl_pre_save_reciever, sender=Post)
post_save.connect(rl_post_save_reciever, sender=Post)

class movies(models.Model):
	movie_id = models.IntegerField(default=0)
	imdb_id = models.IntegerField(default=0)
	movie_name = models.CharField(max_length=200)
	genre = models.CharField(max_length=200)
	vectors = models.CharField(max_length=200)

class links(models.Model):
	movie_id = models.IntegerField(default=0)
	url = models.CharField(max_length=300)

class meansize(models.Model):
	movie_id = models.IntegerField(default=0)
	size = models.FloatField(default=0.0)
	mean = models.FloatField(default=0.0)