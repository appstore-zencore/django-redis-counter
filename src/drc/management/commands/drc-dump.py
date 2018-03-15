import djclick as click
from django.apps import apps
from drc.storage import connections


@click.command()
def drc_dump():
    connections.dump()
