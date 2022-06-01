import asyncio
import time
from asyncio.coroutines import iscoroutinefunction


def coast_time(func):
    def fun(*args, **kwargs):
        t = time.perf_counter()
        result = func(*args, **kwargs)
        print(f'func {func.__name__} coast time:{time.perf_counter() - t:.8f} s')
        return result

    async def func_async(*args, **kwargs):
        t = time.perf_counter()
        result = await func(*args, **kwargs)
        print(f'func {func.__name__} coast time:{time.perf_counter() - t:.8f} s')
        return result

    if iscoroutinefunction(func):
        return func_async
    else:
        return fun


@coast_time
def test():
    print('func start')
    time.sleep(2)
    print('func end')


@coast_time
async def test_async():
    print('async func start')
    await asyncio.sleep(2)
    print('async func end')


if __name__ == '__main__':
    test()
    asyncio.get_event_loop().run_until_complete(test_async())
