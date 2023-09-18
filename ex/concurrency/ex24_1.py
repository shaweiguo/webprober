import dramatiq
import time
from loguru import logger
from ex24 import wait


logger.info(f"Start program")
# [wait.send(i, 10) for i in range(10)]
g = dramatiq.group([
    wait.message(10, 'A'),
    wait.message(5, 'B'),
    wait.message(4, 'C'),
    wait.message(7, 'D'),
]).run()
for res in g.get_results(block=True, timeout=12000):
    logger.info(res)
logger.info(f"End program")
