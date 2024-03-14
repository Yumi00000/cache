from pymemcache.client.base import Client

mc = Client(('localhost', 11211))


def cached_func(expire=None):
    if expire is None:
        expire = 0

    def deco_c(func):
        def wrapper(*args, **kwargs):
            key = args[0]
            cache_val = mc.get(str(key), None)
            if cache_val is not None:
                return int(cache_val)
            result = func(*args, **kwargs)
            mc.set(str(key), str(result), expire=3)
            return result

        return wrapper

    return deco_c


@cached_func(expire=30)
def fib(a):
    if a < 0:
        raise ValueError('a must be greater than 0')
    elif a == 0:
        return 0
    elif a == 1:
        return 1
    else:
        return fib(a - 1) + fib(a - 2)


if __name__ == '__main__':
    print(fib(40))
