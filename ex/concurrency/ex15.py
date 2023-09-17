import time
import math
import numpy as np
from multiprocessing.pool import Pool

def func(value):
    result = math.sqrt(value)
    print(f"The value {value} and the elaboration is {result}")
    time.sleep(value)
    return result

if __name__ == "__main__":
    with Pool() as pool:
        data = np.array([10, 3, 6, 1, 4, 5, 2, 9, 7, 3, 4, 6])
        results = pool.map(func, data, chunksize=4)
        print("The main process is going on...")
        for result in results:
            print(f"This is the result: {result}")
    print("END Program")
