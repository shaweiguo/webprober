import time
import math
import os
import numpy as np
from concurrent.futures import ProcessPoolExecutor

def func(value):
    result = math.sqrt(value)
    pid = os.getpid()
    print(f"[{pid}] The value {value} and the elaboration is {result}")
    time.sleep(value)
    return result

if __name__ == "__main__":
    with ProcessPoolExecutor(10) as executor:
        data = np.array([10, 3, 6, 1, 4, 5, 2, 9, 7, 3, 4, 6])
        for result in executor.map(func, data, chunksize=4):
            print(f"This is the result: {result}")
    print("END Program")
