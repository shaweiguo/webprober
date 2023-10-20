import asyncio
from concurrent.futures import ThreadPoolExecutor
import functools
from queue import Queue
from threading import Lock, RLock, Thread
import socket
import threading
import time
import tkinter
from tkinter import Entry, Label, Tk, ttk
from typing import Callable, List, Optional
from aiohttp import ClientSession
from loguru import logger
import requests

from util.delay import async_timed


def echo(client: socket):
    while True:
        data = client.recv(1024)
        logger.info(f'Received data: {data}, sending!')
        client.sendall(data)


class ClientEchoThread(Thread):
    def __init__(self, client: socket):
        super().__init__()
        self._client = client

    def run(self):
        try:
            while True:
                data = self._client.recv(1024)
                if not data:
                    raise BrokenPipeError('Connection closed')
                logger.info(f'Received data: {data}, sending!')
                self._client.sendall(data)
        except OSError as e:
            logger.error(
                f'Thread interrupted by {e} exception, shutting down!')

    def close(self):
        if self.is_alive():
            self._client.sendall(bytes('Shutting down!', encoding='utf-8'))
            self._client.shutdown(socket.SHUT_RDWR)


def server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_address = ('localhost', 8000)
        server.bind(server_address)
        server.listen()

        client_threads = []
        try:
            while True:
                client, _ = server.accept()
                logger.info(f'Connection from {client}')
                # thread = Thread(target=echo, args=(client,), daemon=True)
                thread = ClientEchoThread(client)
                client_threads.append(thread)
                thread.start()
        except KeyboardInterrupt:
            logger.error('Shutting down!')
            [thread.close() for thread in client_threads]


def get_status_code(url: str) -> int:
    response = requests.get(url)
    return f'{threading.current_thread().name}/{response.status_code}'


def example_status() -> None:
    url = 'https://www.example.com'
    logger.info(f'{get_status_code(url)}')
    logger.info(f'{get_status_code(url)}')


def async_example_status() -> None:
    start = time.time()
    with ThreadPoolExecutor() as pool:
        urls = ['https://www.example.com' for _ in range(100)]
        results = pool.map(get_status_code, urls)
        for result in results:
            logger.info(f'{result}')
    end = time.time()
    logger.info(f'finished requests in {end - start:.4f} second(s).')


@async_timed()
async def asyncio_threadpool() -> None:
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        urls = ['https://www.example.com' for _ in range(100)]
        tasks = [
            loop.run_in_executor(
                pool,
                functools.partial(get_status_code, url)
            )
            for url in urls
        ]
        results = await asyncio.gather(*tasks)
        logger.info(f'{results}')


@async_timed()
async def tothread() -> None:
    urls = ['https://www.example.com' for _ in range(100)]
    tasks = [
        asyncio.to_thread(get_status_code, url)
        for url in urls
    ]
    results = await asyncio.gather(*tasks)
    logger.info(f'{results}')


counter: int = 0
counter_lock = Lock()


def get_status_code_with_lock(url: str) -> int:
    global counter
    response = requests.get(url)
    with counter_lock:
        counter += 1
    return f'{threading.current_thread().name}/{response.status_code}'


async def reporter(request_count: int) -> None:
    while counter < request_count:
        logger.info(f'Finished {counter}/{request_count} requests.')
        await asyncio.sleep(.5)


@async_timed()
async def tothread_with_lock0() -> None:
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        request_count = 200
        urls = ['https://www.example.com' for _ in range(request_count)]
        reporter_task = asyncio.create_task(reporter(request_count))
        tasks = [
            loop.run_in_executor(
                pool,
                functools.partial(get_status_code_with_lock, url)
            )
            for url in urls
        ]
        results = await asyncio.gather(*tasks)
        logger.info(f'{results}')
        await reporter_task


@async_timed()
async def tothread_with_lock() -> None:
    request_count = 200
    urls = ['https://www.example.com' for _ in range(request_count)]
    reporter_task = asyncio.create_task(reporter(request_count))
    tasks = [
        asyncio.to_thread(get_status_code_with_lock, url)
        for url in urls
    ]
    results = await asyncio.gather(*tasks)
    await reporter_task
    logger.info(f'{results}')


list_lock = RLock()


def sum_list(int_list: List[int]) -> int:
    logger.info('Waiting to acquire lock...')
    with list_lock:
        logger.info('Acquired lock.')
        if len(int_list) == 0:
            logger.info('Finished summing.')
            return 0
        else:
            head, *tail = int_list
            logger.info('Summing rest of list.')
            return head + sum_list(tail)


def sum() -> None:
    thread = Thread(target=sum_list, args=([1, 2, 3, 4], ))
    thread.start()
    thread.join()


class IntListThreadsafe:
    def __init__(self, wrapped_list: List[int]):
        self._lock = RLock()
        self._inner_list = wrapped_list

    def indices_of(self, to_find: int) -> List[int]:
        with self._lock:
            enumerator = enumerate(self._inner_list)
            return [index for index, value in enumerator if value == to_find]

    def find_and_replace(
            self,
            to_replace: int,
            replace_with: int,
    ) -> None:
        with self._lock:
            indices = self.indices_of(to_replace)
            for index in indices:
                self._inner_list[index] = replace_with

    def display(self) -> None:
        logger.info(f'{self._inner_list}')


def intlist_replace() -> None:
    threadsafe_list = IntListThreadsafe([1, 2, 1, 2, 1])
    threadsafe_list.find_and_replace(1, 2)
    threadsafe_list.display()


def tk_window() -> None:
    window = tkinter.Tk()
    window.title('Hello world app')
    window.geometry('200x100')

    def say_hello():
        logger.info('Hello tk!')

    hello_button = ttk.Button(window, text='Say hello', command=say_hello)
    hello_button.pack()

    window.mainloop()


class StressTest:
    def __init__(
            self,
            loop: asyncio.AbstractEventLoop,
            url: str,
            total_requests: int,
            callback: Callable[[int, int], None]
    ) -> None:
        self._completed_requests: int = 0
        self._load_test_future: Optional[asyncio.Future] = None
        self._loop = loop
        self._url = url
        self._total_requests = total_requests
        self._callback = callback
        self._refresh_rate = total_requests // 100

    def start(self):
        future = asyncio.run_coroutine_threadsafe(
            self._make_requests(),
            self._loop)
        self._load_test_future = future

    def cancel(self):
        if self._load_test_future:
            self._loop.call_soon_threadsafe(self._load_test_future.cancel)

    async def _get_url(self, session: ClientSession, url: str):
        try:
            await session.get(url)
        except Exception as e:
            logger.error(e)
        self._completed_requests += 1
        if self._completed_requests % self._refresh_rate == 0 \
                or self._completed_requests == self._total_requests:
            self._callback(self._completed_requests, self._total_requests)

    async def _make_requests(self):
        async with ClientSession() as session:
            reqs = [
                self._get_url(session, self._url)
                for _ in range(self._total_requests)]
            await asyncio.gather(*reqs)


class LoadTester(Tk):
    def __init__(self, loop, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self._queue = Queue()
        self._refresh_ms = 25

        self._loop = loop
        self._load_test: Optional[StressTest] = None
        self.title('URL Requester')

        self._url_label = Label(self, text="URL:")
        self._url_label.grid(column=0, row=0)
        self._url_field = Entry(self, width=30, show='https://example.com')
        self._url_field.grid(column=1, row=0)

        self._request_label = Label(self, text="Number of requests:")
        self._request_label.grid(column=0, row=1)
        self._request_field = Entry(self, width=10)
        self._request_field.grid(column=1, row=1)

        self._submit = ttk.Button(self, text="Submit", command=self._start)
        self._submit.grid(column=2, row=1)

        self._pb_label = Label(self, text="Progress:")
        self._pb_label.grid(column=0, row=3)
        self._pb = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate")
        self._pb.grid(column=1, row=3, columnspan=2)

    def _update_bar(self, pct: int):
        if pct == 100:
            self._load_test = None
            self._submit['text'] = 'Submit'
        else:
            self._pb['value'] = pct
            self.after(self._refresh_ms, self._poll_queue)

    def _queue_update(self, completed_requests: int, total_requests: int):
        self._queue.put(int(completed_requests / total_requests * 100))

    def _poll_queue(self):
        if not self._queue.empty():
            percent_complete = self._queue.get()
            self._update_bar(percent_complete)
        else:
            if self._load_test:
                self.after(self._refresh_ms, self._poll_queue)

    def _start(self):
        if self._load_test is None:
            self._submit['text'] = 'Cancel'
            test = StressTest(self._loop,
                              self._url_field.get(),
                              int(self._request_field.get()),
                              self._queue_update)
            self.after(self._refresh_ms, self._poll_queue)
            test.start()
            self._load_test = test
        else:
            self._load_test.cancel()
            self._load_test = None
            self._submit['text'] = 'Submit'


class ThreadedEventLoop(Thread):
    def __init__(self, loop: asyncio.AbstractEventLoop):
        super().__init__()
        self._loop = loop
        self.daemon = True

    def run(self) -> None:
        self._loop.run_forever()


def thread_window() -> None:
    loop = asyncio.new_event_loop()
    asyncio_thread = ThreadedEventLoop(loop)
    asyncio_thread.start()

    app = LoadTester(loop)
    app.mainloop()


if __name__ == '__main__':
    # server()
    # asyncio.run(tothread_with_lock())
    # intlist_replace()
    thread_window()
