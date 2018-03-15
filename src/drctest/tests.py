import json
import redis
from django.test import TestCase
from django.test import Client
from django.urls import reverse
from .models import Page
from .models import PageCounter

class TestDrc(TestCase):

    def setUp(self):
        db = redis.Redis()
        db.flushall()
        self.p1 = Page()
        self.p1.title = "t1"
        self.p1.save()
        self.p1url = reverse("drctest.display_page", args=[self.p1.pk])

    def test01(self):
        browser = Client()
        for i in range(0, 10):
            response = browser.get(self.p1url)
            data = json.loads(response.content)
            assert data["id"] == self.p1.pk
            assert data["title"] == self.p1.title
            assert data["count"] == i+1
