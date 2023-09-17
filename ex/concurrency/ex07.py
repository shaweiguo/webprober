from threading import Thread, Condition
import time
import random


shared = 1
count = 5
condition = Condition()

class Consumer(Thread):
    def __init__(self, count):
        super().__init__()
        global condition
        self.__count = count
    
    def run(self) -> None:
        global shared
        for i in range(self.__count):
            with condition:
                if shared == 0:
                    condition.wait()
                print(f"consumer has used this: {shared}")
                shared = 0
                condition.notify()

class Producer(Thread):
    def __init__(self, count):
        super().__init__()
        global condition
        self.__count = count
    
    def request(self):
        time.sleep(1)
        return random.randint(0, 100)
    
    def run(self) -> None:
        global shared
        for i in range(self.__count):
            with condition:
                shared = self.request()
                print(f"producer has loaded this: {shared}")
                condition.wait()
                if shared == 0:
                    condition.notify()


if __name__ == '__main__':
    p = Producer(count)
    c = Consumer(count)
    p.start()
    c.start()
    p.join()
    c.join()