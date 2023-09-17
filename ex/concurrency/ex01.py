import threading
import time


sequence = ""
COUNT = 5
timeA = 5
timeB = 10

def addA():
    global sequence
    for i in range(COUNT):
        time.sleep(timeA)
        sequence = f"{sequence}A"
        print(f"Sequence: {sequence}")

def addB():
    global sequence
    for i in range(COUNT):
        time.sleep(timeB)
        sequence = f"{sequence}B"
        print(f"Sequence: {sequence}")


if __name__ == "__main__":
    t1 = threading.Thread(target=addA)
    t2 = threading.Thread(target=addB)
    t1.start()
    t2.start()
    t1.join()
    t2.join()