from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Menu(models.Model):
    title = models.CharField(max_length=255, unique=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE,)
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title) if not self.slug else self.slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'
