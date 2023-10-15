import multiprocessing
from typing import List
import asyncpg
import asyncio
from loguru import logger


CREATE_BRAND_TABLE = \
    """
    CREATE TABLE IF NOT EXISTS brand(
        brand_id SERIAL PRIMARY KEY,
        brand_name TEXT NOT NULL
    );
    """
CREATE_PRODUCT_TABLE = \
    """
    CREATE TABLE IF NOT EXISTS product(
        product_id SERIAL PRIMARY KEY,
        product_name TEXT NOT NULL,
        brand_id INT NOT NULL,
        FOREIGN KEY (brand_id) REFERENCES brand(brand_id)
    );
    """
CREATE_PRODUCT_COLOR_TABLE = \
    """
    CREATE TABLE IF NOT EXISTS product_color(
        product_color_id SERIAL PRIMARY KEY,
        product_color_name TEXT NOT NULL
    );
    """
CREATE_PRODUCT_SIZE_TABLE = \
    """
    CREATE TABLE IF NOT EXISTS product_size(
        product_size_id SERIAL PRIMARY KEY,
        product_size_name TEXT NOT NULL
    );
    """
CREATE_SKU_TABLE = \
    """
    CREATE TABLE IF NOT EXISTS sku(
        sku_id SERIAL PRIMARY KEY,
        product_id INT NOT NULL,
        product_size_id INT NOT NULL,
        product_color_id INT NOT NULL,
        FOREIGN KEY (product_id)
        REFERENCES product(product_id),
        FOREIGN KEY (product_size_id)
        REFERENCES product_size(product_size_id),
        FOREIGN KEY (product_color_id)
        REFERENCES product_color(product_color_id)
    );
    """
COLOR_INSERT = \
    """
    INSERT INTO product_color VALUES(1, 'Blue');
    INSERT INTO product_color VALUES(2, 'Black');
    """
SIZE_INSERT = \
    """
    INSERT INTO product_size VALUES(1, 'Small');
    INSERT INTO product_size VALUES(2, 'Medium');
    INSERT INTO product_size VALUES(3, 'Large');
    """


async def init() -> None:
    connection = await asyncpg.connect(
        host='localhost',
        port=5432,
        database='test',
        user='postgres',
        password='q1w2e3r4',
    )
    version = connection.get_server_version()
    logger.info(f'Connected! Postgres server version is {version}')

    statements = [
        CREATE_BRAND_TABLE,
        CREATE_PRODUCT_TABLE,
        CREATE_PRODUCT_COLOR_TABLE,
        CREATE_PRODUCT_SIZE_TABLE,
        CREATE_SKU_TABLE,
        SIZE_INSERT,
        COLOR_INSERT,
    ]
    logger.info('Creating product database...')
    for statement in statements:
        status = await connection.execute(statement)
        logger.info(f'{status}')
    logger.info('Finished creating the product database!')

    await connection.close()


async def brand() -> None:
    connection = await asyncpg.connect(
        host='localhost',
        port=5432,
        database='test',
        user='postgres',
        password='q1w2e3r4',
    )
    await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'Levis')")
    await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'Seven')")
    brand_query = 'SELECT brand_id, brand_name FROM brand'
    results: List[asyncpg.Record] = await connection.fetch(brand_query)
    for brand in results:
        logger.info(f'id: {brand["brand_id"]} name: {brand["brand_name"]}')

    await connection.close()


if __name__ == '__main__':
    logger.info(f'{multiprocessing.cpu_count()} processors.')
    # asyncio.run(brand())
