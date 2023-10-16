import functools
import time
from concurrent.futures import ProcessPoolExecutor
from loguru import logger
import asyncio
from asyncio.events import AbstractEventLoop
from functools import partial
from typing import List, Dict


def count(count_to: int) -> int:
    start = time.time()
    counter = 0
    while counter < count_to:
        counter += 1
    end = time.time()
    logger.info(
        f'Finished counting to {count_to} in {end - start:.6f} seconds.')
    return counter


async def async_counter() -> None:
    with ProcessPoolExecutor() as executor:
        loop: AbstractEventLoop = asyncio.get_running_loop()
        nums = [1, 3, 5, 22, 100000000]
        calls: List[partial[int]] = [partial(count, num) for num in nums]
        call_coros = []

        for call in calls:
            call_coros.append(loop.run_in_executor(executor, call))

        results = await asyncio.gather(*call_coros)

        for result in results:
            logger.info(f'Result: {result}')


def map_frequency(text: str) -> Dict[str, int]:
    words = text.split(' ')
    frequencies = {}
    for word in words:
        if word in frequencies:
            frequencies[word] += 1
        else:
            frequencies[word] = 1
    return frequencies


def merge_dictionaries(first: Dict[str, int],
                       second: Dict[str, int]) -> Dict[str, int]:
    merged = first
    for key in second:
        if key in merged:
            merged[key] += second[key]
        else:
            merged[key] = second[key]
    return merged


def word_count() -> None:
    lines = [
        "I know what I know",
        "I know that I know",
        "I don't know much",
        "They don't know much",
    ]
    mapped_results = [map_frequency(line) for line in lines]

    for result in mapped_results:
        logger.info(f'Result: {result}')

    logger.info(f'{functools.reduce(merge_dictionaries, mapped_results)}')


def googlebooks_count() -> None:
    data_path = '/home/sha/Downloads/googlebooks-eng-all-1gram-20120701-a'
    freqs = {}
    with open(data_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        start = time.time()
        for line in lines:
            data = line.split('\t')
            word = data[0]
            count = int(data[2])
            if word in freqs:
                freqs[word] += count
            else:
                freqs[word] = count
        end = time.time()
        logger.info(f'{end - start:.4f}')


def partition(data: List,
              chunk_size: int) -> List:
    for i in range(0, len(data), chunk_size):
        yield data[i: i + chunk_size]


def map_frequencies(chunk: List[str]) -> Dict[str, int]:
    counter = {}
    for line in chunk:
        word, _, count, _ = line.split('\t')
        if counter.get(word):
            counter[word] += int(count)
        else:
            counter[word] = int(count)
    return counter


async def reduce(loop, pool, counters, chunk_size) -> Dict[str, int]:
    chunks: List[List[Dict]] = list(partition(counters, chunk_size))
    reducers = []
    while len(chunks[0]) > 1:
        for chunk in chunks:
            reducer = functools.partial(
                functools.reduce, merge_dictionaries, chunk)
            reducers.append(loop.run_in_executor(pool, reducer))
        reducer_chunks = await asyncio.gather(*reducers)
        chunks = list(partition(reducer_chunks, chunk_size))
        reducers.clear()
    return chunks[0][0]


async def async_googlebooks_count(partition_size: int) -> None:
    data_path = '/home/sha/Downloads/googlebooks-eng-all-1gram-20120701-a'
    with open(data_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        loop = asyncio.get_running_loop()
        tasks = []
        with ProcessPoolExecutor() as pool:
            start = time.time()
            for chunk in partition(lines, partition_size):
                tasks.append(
                    loop.run_in_executor(
                        pool, functools.partial(map_frequencies, chunk)))
            intermediate_results = await asyncio.gather(*tasks)
            final_results = await reduce(loop, pool, intermediate_results, 500)
            a_word = 'Aardvark'
            logger.info(
                f'{a_word} has appeared {final_results[a_word]} times.')
            end = time.time()
            logger.info(
                f'MapReduce({partition_size}) took: '
                f'{end - start:.4f} seconds.')


if __name__ == '__main__':
    # asyncio.run(async_counter())
    # 2023-10-16 17:10:30.082 | INFO     |
    #  __main__:googlebooks_count:90 - 37.3714
    # googlebooks_count()
    asyncio.run(async_googlebooks_count(partition_size=60000))
