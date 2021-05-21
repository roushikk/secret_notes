import nanoid
from django.db import models
from django.shortcuts import reverse


def generate_slug():
    return nanoid.generate(size=12)


class Note(models.Model):
    slug = models.SlugField(default=generate_slug, unique=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    password = models.CharField(max_length=80, blank=True, null=True)
    allowed_reads = models.IntegerField(default=1)
    times_read = models.IntegerField(default=0)
    display_confirmation = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('note', kwargs={'slug': self.slug})
