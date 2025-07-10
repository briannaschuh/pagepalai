import asyncio
from functools import partial

async def run_in_threadpool(func, *args, **kwargs):
    """
    Runs a sync function inside an async context using a threadpool.
    """
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, partial(func, *args, **kwargs))