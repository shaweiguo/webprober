import threading
import time


shared_data = 0
lock = threading.Lock()

def funcA():
    global shared_data
    for i in range(10):
        local = shared_data
        local += 10
        time.sleep(1)
        shared_data = local
        print(f"Thread A wrote: {shared_data}, {i}")
        lock.acquire()

def funcB():
    global shared_data
    lock.acquire()
    for i in range(10):
        local = shared_data
        local -= 10
        time.sleep(1)
        shared_data = local
        print(f"Thread B wrote: {shared_data}, {i}")
        lock.release()

if __name__ == "__main__":
    ta = threading.Thread(target=funcA)
    tb = threading.Thread(target=funcB)
    ta.start()
    tb.start()
    ta.join()
    tb.join()