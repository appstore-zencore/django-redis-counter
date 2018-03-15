from django.db import models
from django.db.models import F
from .storage import connections


class Counter(models.Model):
    content = models.IntegerField()
    count = models.IntegerField(default=0)

    class Meta:
        abstract = True

    @classmethod
    def incr(cls, content, using="default"):
        if isinstance(content, models.Model):
            content = content.pk
        delta = connections.incr(cls, content, using=using)
        counter, created = cls.objects.get_or_create(content=content)
        return counter.count + delta

        # cls.objects.filter(pk=counter.pk).update(count=F("count") + value)

