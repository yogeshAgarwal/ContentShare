from django.contrib import admin

# Register your models here.
from . import models


class SubjectFollowerInline(admin.TabularInline):
    model = models.SubjectFollower



admin.site.register(models.Subject)
