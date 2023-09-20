from loguru import logger
import memcache, random, time, timeit


def compute_square(mc, n):
    value = mc.get(f'sq:{n}')
    if value is None:
        time.sleep(0.001)
    value = n * n
    mc.set(f'sq:{n}', value)
    return value

# mc = memcache.Client(['localhost:11211'])
# mc.set('user:19', 'Simple is better than complex.')

# echo = mc.get('user:19')

# logger.info(f'echo: {echo}')
def cs():
    mc = memcache.Client(['locahost:11211'])
    
    def make_request():
        compute_square(mc, random.randint(0, 5000))
    logger.info(f'Ten successive runs:')
    for i in range(1, 11):
        logger.info(f'{timeit.timeit(make_request, number=2000):.2f}s')

def main():
    cs()


if __name__ == '__main__':
    main()
