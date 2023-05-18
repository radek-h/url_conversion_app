from django.db import models


class URL(models.Model):
    full_url = models.URLField(unique=True, null=True)
    full_shorten_url = models.URLField(unique=True, null=True)
    url_shorten_key = models.CharField(max_length=5, unique=True, null=True)
