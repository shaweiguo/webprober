from multiprocessing import Process, Queue
import time
import random

class Consumer(Process):
    def __init__(self, count, queue):
        super().__init__()
        self.__count = count
        self.__queue = queue
    
    def run(self) -> None:
        global queue
        for i in range(self.__count):
            local = self.__queue.get()
            time.sleep(2)
            print(f"consumer has used this: {local}")

class Producer(Process):
    def __init__(self, count, queue):
        super().__init__()
        self.__count = count
        self.__queue = queue
    
    def request(self):
        time.sleep(1)
        return random.randint(0, 100)
    
    def run(self) -> None:
        for i in range(self.__count):
            local = self.request()
            self.__queue.put(local)
            print(f"producer has loaded this: {local}")


if __name__ == '__main__':
    queue = Queue()
    count = 5
    p1 = Producer(count, queue)
    p2 = Producer(count, queue)
    c1 = Consumer(count, queue)
    c2 = Consumer(count, queue)
    p1.start()
    p2.start()
    c1.start()
    c2.start()
    p1.join()
    p2.join()
    c1.join()
    c2.join()