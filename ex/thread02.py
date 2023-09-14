import concurrent.futures
import time
import random

def thread(num, t):
    print(f"Thread {num} started")
    print(f"Thread {num} will sleep for {t} seconds")
    time.sleep(t)
    print(f"Thread {num} ended")

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    for i in range(4):
        executor.submit(thread(i, random.randint(1, 5)))

print("Programd ended")