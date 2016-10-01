# encoding=utf8


class ExcCodes(object):

    EXC_CODE_UNDEFINED = 0
    CANNOT_FOUND_PRIMARY_KEY = 1

    MSG_MAP = {
        EXC_CODE_UNDEFINED: u'Exception code undefined.',
        CANNOT_FOUND_PRIMARY_KEY: u'Cannot found primary key: `id` in class, please ensure this class has field named `id`.',
    }


class CacheException(Exception):

    def __init__(self, exc_code):
        msg = ExcCodes.MSG_MAP.get(exc_code)
        if not msg:
            msg = ExcCodes.MSG_MAP.get(ExcCodes.EXC_CODE_UNDEFINED)
        return super(BaseException, self).__init__(msg)


def raise_exc(exc_code):
    raise CacheException(exc_code)
