from django.db import models
from drc.models import Counter


class Page(models.Model):
    title = models.CharField(max_length=32)

class PageCounter(Counter):
    pass

