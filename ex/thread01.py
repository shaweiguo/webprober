import threading
import time

def func(i):
    print(f"start thread {i}")
    time.sleep(2)
    print(f"end thread {i}")
    return

n_threads = 5
threads = []

for i in range(n_threads):
    t = threading.Thread(target=func, args=(i,))
    threads.append(t)
    t.start()

for i in range(n_threads):
    threads[i].join()