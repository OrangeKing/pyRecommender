import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible


# Create your models here.
@python_2_unicode_compatible
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    contents = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=120, null=True, blank=True)
    # slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.title

    def was_published_recently(self):
        return self.timestamp >= timezone.now() - datetime.timedelta(days=1) 

    # @property
    # def title(self):
    #     return self.name
