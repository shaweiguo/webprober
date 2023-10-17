import asyncio
from asyncio import Queue
from random import randrange
from typing import List
from loguru import logger


class Product:
    def __init__(self, name: str, checkout_time: float) -> None:
        self._name = name
        self._checkout_time = checkout_time


class Customer:
    def __init__(self, customer_id: int, products: List[Product]) -> None:
        self._customer_id = customer_id
        self._products = products


async def checkout_customer(queue: Queue, cashier_num: int) -> None:
    while not queue.empty():
        customer: Customer = queue.get_nowait()
        logger.info(f"Cashier {cashier_num} "
                    f"checking out customer "
                    f"{customer._customer_id}")
        for product in customer._products:
            logger.info(f"Cashier {cashier_num} "
                        f"checking out customer "
                        f"{customer._customer_id}'s {product._name}")
            await asyncio.sleep(product._checkout_time)
        logger.info(f"Cashier {cashier_num} "
                    f"finished checking out customer "
                    f"{customer._customer_id}")
        queue.task_done()


async def supermarket() -> None:
    customer_queue = Queue()
    all_products = [
        Product('beer', 2),
        Product('bananas', .5),
        Product('sausage', .2),
        Product('diapers', .2),
    ]
    for i in range(10):
        products = [all_products[randrange(len(all_products))]
                    for _ in range(randrange(10))]
        customer_queue.put_nowait(Customer(i, products))
    cashiers = [asyncio.create_task(checkout_customer(customer_queue, i))
                for i in range(3)]
    await asyncio.gather(customer_queue.join(), *cashiers)


asyncio.run(supermarket())
