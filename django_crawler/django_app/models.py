from django.db import models

# Create your models here.


class Article(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField(null=True, blank=True)