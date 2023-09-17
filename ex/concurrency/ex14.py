from multiprocessing import Process, Pipe
import time
import random

class Consumer(Process):
    def __init__(self, count, conn):
        super().__init__()
        self.__count = count
        self.__conn = conn
    
    def run(self) -> None:
        global queue
        for i in range(self.__count):
            local = self.__conn.recv()
            time.sleep(2)
            print(f"consumer has used this: {local}")

class Producer(Process):
    def __init__(self, count, conn):
        super().__init__()
        self.__count = count
        self.__conn = conn
    
    def request(self):
        time.sleep(1)
        return random.randint(0, 100)
    
    def run(self) -> None:
        for i in range(self.__count):
            local = self.request()
            self.__conn.send(local)
            print(f"producer has loaded this: {local}")


if __name__ == '__main__':
    recver, sender = Pipe()
    count = 5
    p1 = Producer(count, sender)
    c1 = Consumer(count, recver)
    p1.start()
    c1.start()
    p1.join()
    c1.join()
    recver.close()
    sender.close()
