from threading import Thread, Semaphore
import time
import random


shared = 1
count = 5
semaphore = Semaphore(1)

class Consumer(Thread):
    def __init__(self, count):
        super().__init__()
        global semaphore
        self.__count = count
    
    def run(self) -> None:
        global shared
        for i in range(self.__count):
            with semaphore:
                print(f"consumer has used this: {shared}")
                shared = 0

class Producer(Thread):
    def __init__(self, count):
        super().__init__()
        global semaphore
        self.__count = count
    
    def request(self):
        time.sleep(1)
        return random.randint(0, 100)
    
    def run(self) -> None:
        global shared
        for i in range(self.__count):
            with semaphore:
                shared = self.request()
                print(f"producer has loaded this: {shared}")


if __name__ == '__main__':
    p = Producer(count)
    c = Consumer(count)
    p.start()
    c.start()
    p.join()
    c.join()