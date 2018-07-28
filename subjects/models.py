from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.

import misaka
from django.contrib.auth import get_user_model
User = get_user_model()

# https://docs.djangoproject.com/en/1.11/howto/custom-template-tags/#inclusion-tags
# This is for the in_followers_members check template tag
from django import template
register = template.Library()


class Subject(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    followers = models.ManyToManyField(User,through="SubjectFollower")



    def __str__(self):
        return self.name



    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)



    def get_absolute_url(self):
        return reverse("subjects:single", kwargs={"slug": self.slug})


    class Meta:
        ordering = ["name"]






class SubjectFollower(models.Model):
    subject = models.ForeignKey(Subject, related_name="following", on_delete=models.CASCADE,)
    user = models.ForeignKey(User,related_name='follwed_topics', on_delete=models.CASCADE,)
    def __str__(self):
        return self.user.username
    class Meta:
        unique_together = ("subject", "user")
