import functools

import os


def debug(fn):
    if not os.getenv('LOCAL'):
        return fn

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        print('DEBUG: {}({}) -> '.format(
            fn.__name__,
            ', '.join(
                list(map(str, args)) +
                ['{}={}'.format(k, str(v)) for k, v in kwargs.items()]
            )
        ), end='')
        ret = fn(*args, **kwargs)
        print(ret)
        return ret

    return wrapper


if __name__ == '__main__':
    @debug
    def some_function(a: int, b: int, c: int = 0):
        return a * b + c


    print(some_function(5, b=3, c=1))
