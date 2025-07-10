import inspect

def method_name():
    """
    Returns the name of teh calling function/method
    """
    return inspect.currentframe().f_back.f_code.co_name