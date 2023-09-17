import multiprocessing
import time

def function(i):
    print(f"start Process {i}")
    time.sleep(1)
    print(f"end Process {i}")
    return


if __name__ == "__main__":
    processes = []
    n_procs = 5
    for i in range(n_procs):
        p = multiprocessing.Process(target=function, args=(i,))
        processes.append(p)
        p.start()
    for i in range(n_procs):
        processes[i].join()
    print("End program")
