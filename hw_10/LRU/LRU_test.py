from collections import OrderedDict

class Cache(OrderedDict):
    def __init__(self, max_len):
        super().__init__
        self.max_len = max_len

    def __setitem__(self, key, value):
        if len(self)+1 > self.max_len:
            self.popitem()
        if key in self:
            super().move_to_end(key, last = False)
        else:
            super().__setitem__(key, value)
            super().move_to_end(key, last = False)

            
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)








'''def lru_decorator(func):
    cache = Cache(5)
    def wrapper(args):
        result = func(args)
        return result
    return wrapper'''

@lru_decorator
def fibonacci(n):  
    if n <= 0:  
        return 0  
    elif n == 1:  
        return 1  
    if n not in cache:  
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)  

    return cache[n]  


fibonacci(10)
