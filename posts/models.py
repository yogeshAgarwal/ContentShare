from django.db import models
from django.conf import settings
from django.urls import reverse
from redactor.fields import RedactorField
# Create your models here.


import misaka

from subjects.models import  Subject


from django.contrib.auth import get_user_model
User = get_user_model()

class Post(models.Model):
    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE,)
    created_at = models.DateTimeField(auto_now=True)
    message = RedactorField(verbose_name=u'Yogesh')
    title= models.TextField(max_length=200, null=True)
    message_html = models.TextField(editable=False)
    subject = models.ForeignKey(Subject, related_name="posts",null=True, blank=True, on_delete=models.CASCADE,)

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "posts:single",
            kwargs={
                "username": self.user.username,
                "pk": self.pk
            }
        )

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["user", "message"]
