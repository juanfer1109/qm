from django.db import models
from datetime import date, datetime
from django.contrib.auth.models import User
from django.utils import timezone


class Issue(models.Model):
    ed = models.PositiveIntegerField()
    name = models.CharField(max_length=200)
    release_date = models.DateField()
    published = models.BooleanField(default=False)
    image = models.ImageField()

    class Meta:
        ordering = ["ed"]

    def __str__(self):
        return self.name


class Article(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.SET_NULL, blank=True, null=True)
    headline = models.CharField(max_length=200)
    main_content = models.TextField()
    sec_content = models.TextField(blank=True)
    main_image = models.ImageField(blank=True)
    main_media = models.URLField(blank=True)
    secundary_image = models.ImageField(blank=True)
    secundary_media = models.URLField(blank=True)
    author = models.ForeignKey(User, blank=True, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ["issue"]

    def __str__(self):
        return self.headline
