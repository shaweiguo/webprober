import multiprocessing
import time

def function(i):
    process = multiprocessing.current_process()
    print(f"start Process {i}({process.pid})")
    time.sleep(1)
    print(f"end Process {i}({process.pid})")
    return


if __name__ == "__main__":
    pool = multiprocessing.Pool()
    print(f"Processes started: {pool._processes}")
    
    for i in range(pool._processes):
        results = pool.apply(function, args=(i,))
    pool.close()
    print("End program")
