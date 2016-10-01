# encoding=utf8

import functools
import logging

from redis import RedisError

from .client import RedisWrapper

from .exc import (
    ExcCodes,
    raise_exc,
)

logger = logging.getLogger(__name__)

cache_client = RedisWrapper()


class _CacheMixin(type):

    @staticmethod
    def _deco(func, hook):

        @functools.wraps(func)
        def wrapper(self, *args, **kw):
            result = func(self, *args, **kw)
            try:
                cls = type(self)
                if not hasattr(self, cls._PRIMARY_KEY):
                    raise_exc(ExcCodes.CANNOT_FOUND_PRIMARY_KEY)
                hook(getattr(self, cls._PRIMARY_KEY))
            except RedisError as exc:
                logger.error(exc.message)
            return result

        return wrapper

    def __new__(self, name, bases, attrs):
        cls = type.__new__(self, name, bases, attrs)

        for method, hook in cls._registors:
            origin = getattr(cls, method)
            setattr(cls, method, self._deco(origin, hook))
        return cls


def set_cache(pk):
    print 'Set cache: {}'.format(pk)


def get_cache(pk):
    print 'Get cache: {}'.format(pk)


def update_cache(pk):
    # TODO: get entity and set to cache.
    cache_client.set(pk, '123')


class CacheMixin(_CacheMixin):

    _registors = (
        ('commit', update_cache),
        ('save', update_cache),
        ('update', update_cache),
    )
