import threading
import time


shared = 0
lock = threading.RLock()

def func(name, t):
    global shared
    for i in range(3):
        lock.acquire()
        local = shared
        time.sleep(t)
        for j in range(2):
            lock.acquire()
            local += 1
            time.sleep(1)
            shared = local
            print(f"Thread {name}-{i}/{j} wrote: {shared}")
            lock.release()
        shared = local + 1
        print(f"Thread {name} wrote: {shared}")
        lock.release()

if __name__ == "__main__":
    ta = threading.Thread(target=func, args=('A', 2, ))
    tb = threading.Thread(target=func, args=('B', 8, ))
    tc = threading.Thread(target=func, args=('C', 1, ))
    ta.start()
    tb.start()
    tc.start()
    ta.join()
    tb.join()
    tc.join()