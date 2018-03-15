import logging
import redis
from django.apps import apps
from .settings import DRC_PREFIX
from .settings import DRC_CONNECTIONS


logger = logging.getLogger(__name__)


class Storage(object):

    def __init__(self, prefix, config):
        self.prefix = prefix
        self.config = config
        self.connections = {}

    @property
    def names(self):
        ns = list(self.config.keys())
        ns.sort()
        return ns

    def make_connection(self, connection_config):
        url = connection_config["url"]
        options = {
            "decode_responses": True,
        }
        connection_options = connection_config.get("options", {})
        options.update(connection_options)
        return redis.Redis.from_url(url, **options)

    def get_connection(self, name):
        if not name in self.connections:
            self.connections[name] = self.make_connection(self.config[name])
        return self.connections[name]

    def make_key(self, model, content):
        if isinstance(model, str):
            model_name = model
        else:
            model_name = model._meta.label
        if isinstance(content, (int, str)):
            content_value = str(content)
        else:
            content_value = str(content.pk)
        return ":".join([self.prefix, model_name, content_value])

    def incr(self, model, content, value=1, using="default"):
        save_key = self.make_key(model, content)
        connection = self.get_connection(using)
        return connection.incr(save_key, amount=value)

    def decr(self, model, content, value=1, using="default"):
        save_key = self.make_key(model, content)
        connection = self.get_connection(using)
        return connection.decr(save_key, amount=value)

    def close(self, name=None):
        if name:
            del self.connections[name]
        else:
            self.connections = {}

    def get_items(self, using="default"):
        items = []
        connection = self.get_connection(using)
        for item_key in connection.keys(self.prefix + ":*"):
            value = connection.get(item_key)
            _, model, content = item_key.split(":")
            items.append({
                "model": model,
                "content": int(content),
                "value": int(value),
            })
        return items

    def dump(self):
        for name in self.names:
            items = self.get_items(name)
            for item in items:
                model = item["model"]
                app_label, model_name = model.split(".")
                model = apps.get_model(app_label, model_name)
                content = item["content"]
                value = item["value"]
                model.update(content, value)
                self.decr(model, content, value=value, using=name)

connections = Storage(DRC_PREFIX, DRC_CONNECTIONS)
