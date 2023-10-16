import asyncio
import os
import signal
import socket
from types import TracebackType
import typing

from loguru import logger


async def echo(connection: socket,
               loop: asyncio.AbstractEventLoop) -> None:
    try:
        while data := await loop.sock_recv(connection, 1024):
            if data == b'quit\r\n':
                await loop.sock_sendall(connection, b'Bye!')
                connection.close()
                return
            if data == b'boom\r\n':
                raise Exception('Unexpected network error')
            await loop.sock_sendall(connection, data)
    except Exception as e:
        logger.error(e)
    finally:
        connection.close()


echo_tasks = []


async def listen_for_connections(server_socket: socket,
                                 loop: asyncio.AbstractEventLoop) -> None:
    while True:
        conncection, address = await loop.sock_accept(server_socket)
        conncection.setblocking(False)
        logger.info(f'Got a connection from {address}')
        echo_task = asyncio.create_task(echo(conncection, loop))
        echo_tasks.append(echo_task)


class GracefulExit(SystemExit):
    pass


def shutdown():
    raise GracefulExit()


async def close_echo_tasks(echo_tasks: typing.List[asyncio.Task]):
    waiters = [asyncio.wait_for(task, 2) for task in echo_tasks]
    for task in waiters:
        try:
            await task
        except asyncio.exceptions.TimeoutError:
            pass


async def serve(loop) -> None:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = ('localhost', 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()
    logger.info('Server listening...')

    for signame in {'SIGINT', 'SIGTERM'}:
        loop.add_signal_handler(getattr(signal, signame), shutdown)

    await listen_for_connections(server_socket, loop)


def main():
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(serve(loop))
    except GracefulExit:
        loop.run_until_complete(close_echo_tasks(echo_tasks))
    finally:
        loop.close()


class ConnectedSocket:
    def __init__(self, server_socket):
        self._connection = None
        self._server_socket = server_socket

    async def __aenter__(self):
        logger.info('Entering context manager, waiting for connection')
        loop = asyncio.get_event_loop()
        connection, address = await loop.sock_accept(self._server_socket)
        self._connection = connection
        logger.info(f'Accepted a connection from {address}')
        return self._connection

    async def __aexit__(self,
                        exc_type: typing.Optional[typing.Type[BaseException]],
                        exc_value: typing.Optional[BaseException],
                        exc_tb: typing.Optional[TracebackType]):
        logger.info('Exiting context manager')
        self._connection.close()
        logger.info('Closed connection')


async def async_serve():
    loop = asyncio.get_event_loop()

    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('localhost', 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()

    async with ConnectedSocket(server_socket) as connection:
        data = await loop.sock_recv(connection, 1024)
        logger.info(f'Received data: {data}')


if __name__ == '__main__':
    # main()
    asyncio.run(async_serve())
