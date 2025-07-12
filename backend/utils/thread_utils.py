import asyncio
from functools import partial

async def run_in_threadpool(func, *args, **kwargs):
    """
    Runs a synchronous function inside an async context using a threadpool.

    Args:
        func (Callable): The sync function to run.
        *args: Positional arguments to pass to the function.
        **kwargs: Keyword arguments to pass to the function.

    Returns:
        Any: The return value from the sync function.
    """
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, partial(func, *args, **kwargs))