# encoding=utf8

from mock import MagicMock

from tests.helper import gen_pk
from core.cache import mixin


class OrmClass(object):

    __metaclass__ = mixin.CacheMixin

    _PRIMARY_KEY = 'id'

    def __init__(self):
        self.id = gen_pk()

    def save(self):
        print 'Function `save` has been called.'

    def commit(self):
        print 'Function `commit` has been called.'

    def update(self):
        print 'Function `update` has been called.'


class TestCacheMixin(object):

    def test_save_hook(self, monkeypatch):
        mock_client = MagicMock(set=MagicMock())
        monkeypatch.setattr(mixin, 'cache_client',
                            mock_client)
        orm_obj = OrmClass()
        orm_obj.save()
        mock_client.set.assert_called_with(orm_obj.id, '123')
