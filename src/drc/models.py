from django.db import models
from django.db.models import F
from .storage import connections


class Counter(models.Model):
    content = models.IntegerField()
    count = models.IntegerField(default=0)

    class Meta:
        abstract = True

    @classmethod
    def get_content_pk(cls, content):
        if isinstance(content, models.Model):
            return content.pk
        return int(content)

    @classmethod
    def incr(cls, content, using="default"):
        content = cls.get_content_pk(content)
        delta = connections.incr(cls, content, using=using)
        counter, created = cls.objects.get_or_create(content=content)
        return counter.count + delta

    @classmethod
    def update(cls, content, delta):
        content = cls.get_content_pk(content)
        counter, created = cls.objects.get_or_create(content=content)
        if created:
            counter.count = delta
            counter.save()
        else:
            cls.objects.filter(pk=counter.pk).update(count=F("count") + delta)

