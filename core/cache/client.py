# encoding=utf8

import bz2
import cPickle as pickle

from redis import (
    StrictRedis,
    ConnectionPool,
)

from settings import (
    REDIS_HOST,
    REDIS_PORT
)

connection_pool = ConnectionPool(host=REDIS_HOST, port=REDIS_PORT)


def zloads(x):
    return pickle.loads(bz2.decompress(x))


def zdumps(x):
    return bz2.compress(pickle.dumps(x, pickle.HIGHEST_PROTOCOL), 6)


class RedisWrapper(object):

    def __init__(self, namespace='cache'):
        self.namespace = namespace
        self.client = StrictRedis(
            connection_pool=connection_pool,
            socket_timeout=1,
            socket_connect_timeout=3
        )

    def gen_key(self, raw_key):
        if self.namespace is not None:
            return '{}:{}'.format(self.namespace, raw_key)
        return raw_key

    def get(self, raw_key, loader=zloads):
        ret = self.client.get(self.gen_key(raw_key))
        return loader(ret)

    def set(self, raw_key, value, expire_time, dumper=zdumps):
        return self.client.set(
            self.gen_key(raw_key),
            dumper(value),
            expire_time)
