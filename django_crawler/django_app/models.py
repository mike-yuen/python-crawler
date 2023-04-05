# Standard Library
import uuid

# Third Party Stuff
from django.db import models


class UUIDModel(models.Model):
    """An abstract base class model that makes primary key `id` as UUID
    instead of default auto incremented number.
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    class Meta:
        abstract = True


class TimeStampedUUIDModel(UUIDModel):
    """An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields with UUID as primary_key field.
    """

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class Category(TimeStampedUUIDModel):
    title = models.CharField(max_length=255, null=True, blank=True)
    slug = models.TextField(unique=True, null=True, blank=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE,
                               related_name="child_categories", null=True, blank=True)


class Article(TimeStampedUUIDModel):
    title = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    url = models.TextField(unique=True, null=True, blank=True)
    author = models.CharField(max_length=255, null=True, blank=True)
    published_date = models.DateTimeField(null=True, blank=True)
    categories = models.ManyToManyField(Category, symmetrical=False)
