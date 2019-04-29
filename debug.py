import functools
import os


def debug(fn):
    if not os.getenv('LOCAL'):
        return fn

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        ret = fn(*args, **kwargs)
        print('DEBUG: {}({}) -> '.format(
            fn.__name__,
            ', '.join(
                list(map(str, args)) +
                ['{}={}'.format(k, str(v)) for k, v in kwargs.items()]
            )
        ), end='')
        print(ret)
        return ret

    return wrapper
