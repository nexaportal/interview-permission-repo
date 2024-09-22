from .base import *  # NoQA


# enable Browsable API Renderer
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] += ("rest_framework.renderers.BrowsableAPIRenderer",)  # noqa F405
REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] += (  # noqa F405
    "rest_framework.authentication.SessionAuthentication",
)


INSTALLED_APPS += ["django_extensions", "debug_toolbar"]  # noqa F405


CORS_ALLOW_ALL_ORIGINS = True


INTERNAL_IPS = [  # noqa F405
    "127.0.0.1",
    "localhost",
]


MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa F405
