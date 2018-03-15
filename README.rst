django-redis-counter
====================

Django application that keeps content visit count in redis first, then dump to database via extra job.


Install
-------

::

    pip install django-redis-counter

Dependencies
------------

- django
- redis

Usage
-----

1. Add drc in INSTALLED_APPS in django settings.py. drc is short for django-redis-counter.

::

    INSTALLED_APPS = [
        ...
        'drc',
        ...
    ]

2. Define counter models in app's models.py.

::

    from drc.models import Counter

    class Page(models.Model):
        title = models.CharField(max_length=32)
        ...

    class PageCounter(Counter):
        pass

3. Call incr in views.

::

    def display_page(request, page_id):
        page = Page.objects.get(pk=page_id)
        page_visit_number = PageCounter.incr(page)
        return render(request, "page.html", {
            "page": page,
            "page_visit_number": page_visit_number,
        })

4. Create a script to dump cached data to database. Name the script to page_counter_dump.sh or what ever you like.

::

    #!/bin/bash
    cd /your/project/path
    python manage.py drc-dump

5. Add dump task as schedule job, e.g. crontab job.

::

    * * * * * page_counter_dump.sh # dump the cached data every minutes
    1 * * * * page_counter_dump.sh # dump the cached data every hour.


