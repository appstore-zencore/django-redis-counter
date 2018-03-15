import djclick as click
from django.apps import apps
from drc.storage import connections


@click.command()
def drc_dump():
    for name in connections.names:
        items = connections.get_items(name)
        for item in items:
            model = item["model"]
            app_label, model_name = model.split(".")
            model = apps.get_model(app_label, model_name)
            key = item["key"]
            value = item["value"]
            model.incr(key, value)
            connections.decr(model, key, value=value, using=name)
