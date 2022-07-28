from .base import *
from environs import Env


env = Env()
env.read_env()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', False)

SECRET_KEY = env('DEV_SECRET_KEY',
                 'm$aagdyu#_dyh(epemps!+767i^jz_x2=jtk63im$k5aqp!)4m')

ALLOWED_HOSTS = env.list('DEV_ALLOWED_HOSTS', ['127.0.0.1', 'localhost'])

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = ("127.0.0.1", "172.17.0.1")

try:
    from .local import *
except ImportError:
    pass
