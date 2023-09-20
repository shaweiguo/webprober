import time
from tqdm import tqdm
from tqdm.notebook import trange
import random


def progress1():
    for i in tqdm(range(int(9e6))):
        pass

def progress2():
    for i in tqdm(range(0, 100), desc ="Text You Want"):
        time.sleep(.1)

def progress3():
    for i in tqdm(range(0, 100), total = 500,
              desc ="Text You Want"):
        time.sleep(.1)

def progress4():
    for i in tqdm(range(0, 100), disable = True,
               desc ="Text You Want"):
        time.sleep(.1)
 
    print("Iteration Successful")

def progress5():
    for i in tqdm(range(0, 100), ncols = 100,
               desc ="Text You Want"):
        time.sleep(.1)

def progress6():
    for i in tqdm(range(0, 100), mininterval = 3,
              desc ="Text You Want"):
        time.sleep(.1)

def progress7():
    for i in tqdm(range(0, 100),
              ascii ="123456789$"):
        time.sleep(.1)

def progress8():
    for i in tqdm(range(0, 100), unit =" ticks",
              desc ="Text You Want"):
        time.sleep(.1)

def progress9():
    for i in tqdm(range(0, 100), initial = 50,
              desc ="Text You Want"):
        time.sleep(.1)

# progressive sleep function
def fun(x):
    time.sleep(x)
    return x

def progress10():
    # progress loop
    for i in tqdm(range(10)):
        fun(i)

def progress11():
    for i in tqdm(range(0, 10), desc='Traning Model on 10 Epochs'):
        time.sleep(0.01)
        for x in tqdm(range(0, 10000), desc=f'Epoch {i}'):
            time.sleep(0.0001)

def progress12():
    data = [(i, random.randint(0, 100)) for i in range(0, 100)]
    with tqdm(total=len(data)) as pbar:
        for item in data:
            pbar.set_description(f"Item{item[0]}")
            pbar.refresh()
            t = random.random()
            time.sleep(t)
            pbar.update()

def main():
    progress12()


if __name__ == "__main__":
    main()
