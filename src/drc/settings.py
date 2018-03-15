from django.conf import settings


DRC_PREFIX = getattr(settings, "DRC_PREFIX", "redc")
DRC_CONNECTIONS = getattr(settings, "DRC_CONNECTIONS", {
    "default": {
        "url": "redis://localhost/0",
    }
})
