# Standard Library
import uuid

# Third Party Stuff
from django.db import models


class Article(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    author = models.CharField(max_length=255, null=True, blank=True)
    published_date = models.DateTimeField(null=True, blank=True)
