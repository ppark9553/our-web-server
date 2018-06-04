from __future__ import absolute_import, unicode_literals
from celery.decorators import task

from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

from raven.contrib.django.raven_compat.models import client
