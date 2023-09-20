import numpy as np
from numba import cuda
from loguru import logger

@cuda.jit
def add_one(a):
    tx = cuda.threadIdx.x
    ty = cuda.blockIdx.x
    dim = cuda.blockDim.x

    pos = tx + ty * dim
    if pos < a.size:
        a[pos] += 1

def check():
    n = 10
    a_host = np.random.random(n)
    logger.info(f"Vector a: {a_host}")
    a_dev = cuda.to_device(a_host)
    threads_per_block = 128
    blocks_per_grid = (a_host.size // threads_per_block) + 1
    add_one[threads_per_block, blocks_per_grid](a_dev)

    a_host = a_dev.copy_to_host()
    logger.info(f"New vector a: {a_host}")

@cuda.jit(nopython=True) # Set "nopython" mode for best performance, equivalent to @njit
def go_fast(a): # Function is compiled to machine code when called the first time
    trace = 0.0
    for i in range(a.shape[0]):   # Numba likes loops
        trace += np.tanh(a[i, i]) # Numba likes NumPy functions
    return a + trace              # Numba likes NumPy broadcasting

def check0():
    x = np.arange(100).reshape(10, 10)
    result = go_fast(x)
    print(result)

def main():
    check0()


if __name__ == "__main__":
    main()
