import dramatiq
import time
from loguru import logger
from dramatiq.brokers.redis import RedisBroker
from dramatiq.results import Results
from dramatiq.results.backends import RedisBackend


broker = RedisBroker(host='localhost')
dramatiq.set_broker(broker)
result_backend = RedisBackend(host='localhost')
broker.add_middleware(Results(backend=result_backend))

@dramatiq.actor(store_results=True)
def wait(t, n):
    time.sleep(t)
    logger.info(f"I am the actor {n} and I will wait for {t} seconds")
    return f"I waited for {t} seconds"
