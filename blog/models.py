from collections.abc import Iterable
from django.db import models
from django.utils.text import slugify

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    

class Post(models.Model):

    title = models.CharField(verbose_name = "Title", max_length = 255, unique=True)
    subtitle = models.CharField(verbose_name = "Subtitle", max_length = 255, blank=True)
    slug = models.SlugField(verbose_name = "Slug", max_length = 255, unique=True, blank = True)
    content = models.TextField(verbose_name = "Content")
    meta_description = models.CharField(max_length=150, blank=True)
    date_created = models.DateTimeField(auto_now_add = True)
    date_modified = models.DateTimeField(auto_now = True)
    publish_date = models.DateTimeField(blank = True, null = True)
    published = models.BooleanField(default = False)

    tags = models.ManyToManyField(Tag, blank = True)

    def save(self, *args, **kwargs) -> None:
        if self.slug is None:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
