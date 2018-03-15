import logging
import redis
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

    def make_key(self, model, key):
        if isinstance(model, str):
            model_name = model
        else:
            model_name = model._meta.label
        if isinstance(key, (int, str)):
            key_value = str(key)
        else:
            key_value = str(key.pk)
        return ":".join([self.prefix, model_name, key_value])

    def incr(self, model, key, value=1, using="default"):
        save_key = self.make_key(model, key)
        connection = self.get_connection(using)
        return connection.incr(save_key, amount=value)

    def decr(self, model, key, value=1, using="default"):
        save_key = self.make_key(model, key)
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
            try:
                value = int(connection.get(item_key))
                _, model, key = item_key.split(":")
                items.append({
                    "model": model,
                    "key": key,
                    "value": value,
                })
            except:
                logger.exception("Parse item failed: key={}.".format(item_key))
        return items

connections = Storage(DRC_PREFIX, DRC_CONNECTIONS)
