from django.shortcuts import render
from django.http import JsonResponse
from drc.storage import connections
from .models import Page
from .models import PageCounter


def display_page(request, page_id):
    page = Page.objects.get(pk=page_id)
    count = PageCounter.incr(page)
    data = {
        "id": page.pk,
        "title": page.title,
        "count": count,
    }
    return JsonResponse(data)
