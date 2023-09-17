from threading import Thread
from queue import Queue
import time
import random


shared = 1
count = 5
queue = Queue()

class Consumer(Thread):
    def __init__(self, count):
        super().__init__()
        self.__count = count
    
    def run(self) -> None:
        global queue
        for i in range(self.__count):
            local = queue.get()
            print(f"consumer has used this: {local}")
            queue.task_done()

class Producer(Thread):
    def __init__(self, count):
        super().__init__()
        self.__count = count
    
    def request(self):
        time.sleep(1)
        return random.randint(0, 100)
    
    def run(self) -> None:
        global queue
        for i in range(self.__count):
            local = self.request()
            queue.put(local)
            print(f"producer has loaded this: {local}")


if __name__ == '__main__':
    p1 = Producer(count)
    p2 = Producer(count)
    c1 = Consumer(count)
    c2 = Consumer(count)
    p1.start()
    p2.start()
    c1.start()
    c2.start()
    p1.join()
    p2.join()
    c1.join()
    c2.join()