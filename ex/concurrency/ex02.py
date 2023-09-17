from threading import Thread
import time


sequence = ""
COUNT =5

class SequenceThread(Thread):
    def __init__(self, sleep_time, text):
        super().__init__()
        self.__sleep_time = sleep_time
        self.__text = text
    
    def run(self) -> None:
        global sequence
        for i in range(COUNT):
            time.sleep(self.__sleep_time)
            sequence = f"{sequence}{self.__text}"
            print(f"Sequence: {sequence}")


if __name__ == '__main__':
    ta = SequenceThread(1, 'A')
    tb = SequenceThread(2, 'B')
    ta.start()
    tb.start()
    ta.join()
    tb.join()