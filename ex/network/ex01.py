from loguru import logger
from pymemcache.client import base


client = base.Client(('localhost', 11211))
client.set('hello', 'world')
echo = client.get('hello').decode('utf-8')
logger.info(f"echo of hello: {echo}")