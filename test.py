import functools
from functools import lru_cache


def cache(func):
    """cache function values"""
    @functools.wraps(func)

    def cache_wrapper(*args, **kwargs):
        cache_key = args + tuple(kwargs.items())
        if cache_key not in cache_wrapper.cache.keys():
            cache_wrapper.cache[cache_key] = func(*args, **kwargs)

        return cache_wrapper.cache[cache_key]

    cache_wrapper.cache = dict()
    return cache_wrapper


def counter(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.count += 1
        print(f"Function {func.__name__} has been called {wrapper.count} times")
        return func(*args, **kwargs)
    wrapper.count = 0
    return wrapper


@cache
@counter
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)


