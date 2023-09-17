from threading import Thread, Event
import time
import random


shared = 1
count = 5
event = Event()

class Consumer(Thread):
    def __init__(self, count):
        super().__init__()
        global event
        self.__count = count
    
    def run(self) -> None:
        global shared
        for i in range(self.__count):
            event.wait()
            if shared == 0:
                condition.wait()
            print(f"consumer has used this: {shared}")
            shared = 0
            event.clear()

class Producer(Thread):
    def __init__(self, count):
        super().__init__()
        global event
        self.__count = count
    
    def request(self):
        time.sleep(1)
        return random.randint(0, 100)
    
    def run(self) -> None:
        global shared
        for i in range(self.__count):
            shared = self.request()
            print(f"producer has loaded this: {shared}")
            event.set()


if __name__ == '__main__':
    p = Producer(count)
    c = Consumer(count)
    p.start()
    c.start()
    p.join()
    c.join()