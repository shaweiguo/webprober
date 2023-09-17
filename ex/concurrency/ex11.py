import multiprocessing
import os
import time

def function():
    pid = os.getpid()
    print(f"start Process {pid}")
    time.sleep(1)
    print(f"end Process {pid}")
    return


if __name__ == "__main__":
    processes = []
    n_procs = 5
    for i in range(n_procs):
        p = multiprocessing.Process(target=function)
        processes.append(p)
        p.start()
    for i in range(n_procs):
        processes[i].join()
    print("End program")
