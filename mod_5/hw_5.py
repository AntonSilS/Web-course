
import time
from multiprocessing import Pool
import os

def factorize(*number):
    result = []
    print(f"pid={os.getpid()}, number={number}")
    for num in number:
        result.append([x for x in range(1, num+1) if not num % x])
    return result

if __name__ == '__main__':

    start_1 = time.monotonic()
    with Pool() as pool:
        a, b, c, d = [x[0] for x in pool.map(factorize, (128, 255, 99999, 10651060))]
    end_1 = time.monotonic()
    
    start_2 = time.monotonic()
    a_2, b_2, c_2, d_2 = factorize(128, 255, 99999, 10651060)
    end_2 = time.monotonic()
    
    print(f'Time factorize_mult_process: {end_1 -  start_1}\n')
    print(f'Time factorize: {end_2 -  start_2}\n')
    print(a == a_2, b == b_2, c == c_2, d == d_2)

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
  
