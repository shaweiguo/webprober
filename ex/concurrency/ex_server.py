import selectors
import socket
from typing import List, Tuple

from loguru import logger


def server() -> None:
    selector = selectors.DefaultSelector()
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_addr = ('localhost', 8000)
    server_sock.bind(server_addr)
    server_sock.listen()
    server_sock.setblocking(False)
    selector.register(server_sock, selectors.EVENT_READ)

    while True:
        events: List[
                Tuple[selectors.SelectorKey, int]
            ] = selector.select(timeout=1)
        if len(events) == 0:
            logger.info("No events, waiting a bit more!")
        for event, _ in events:
            event_socket = event.fileobj
            if event_socket == server_sock:
                conn, client_addr = server_sock.accept()
                conn.setblocking(False)
                logger.info(f'Connection from {client_addr}')
                selector.register(conn, selectors.EVENT_READ)
            else:
                data = event_socket.recv(1024)
                logger.info(f'I got data: {data}')
                event_socket.send(data)


def main():
    server()


if __name__ == '__main__':
    main()
