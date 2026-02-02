from django.db import models
from django.conf import settings
from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Bookmark(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)

    # Fechas automáticas (eliminan la necesidad de un método save)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    # Relaciones (on_delete es obligatorio)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks')
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f"{self.title} ({self.url})"


