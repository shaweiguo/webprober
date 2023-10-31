import asyncio
from asyncio import Transport, Future, AbstractEventLoop
from typing import Optional
from loguru import logger


class HTTPGetClientProtocol(asyncio.Protocol):
    def __init__(self, host: str, loop: AbstractEventLoop):
        self._host: str = host
        self._future: Future = loop.create_future()
        self._transport: Optional[Transport] = None
        self._response_buffer: bytes = b''

    async def get_response(self):
        return await self._future

    def _get_request_bytes(self) -> bytes:
        request = f"GET / HTTP/1.1\r\n" \
                  f"Connection: close\r\n" \
                  f"Host: {self._host}\r\n\r\n"
        return request.encode()

    def connection_made(self, transport: Transport):
        logger.info(f"Connection to {self._host} made with "
                    f"{transport.get_extra_info('peername')}")
        self._transport = transport
        self._transport.write(self._get_request_bytes())

    def data_received(self, data: bytes):
        logger.info(f"Received {len(data)} bytes from {self._host}")
        self._response_buffer += data

    def eof_received(self) -> Optional[bool]:
        logger.info(f"Received EOF from {self._host}")
        self._future.set_result(self._response_buffer.decode())
        return False

    def connection_lost(self, exc: Optional[Exception]) -> None:
        if exc is None:
            logger.info("Connection closed without errors.")
        else:
            self._future.set_exception(exc)


async def make_request(host: str, port: int, loop: AbstractEventLoop) -> str:
    def protocol_factory():
        return HTTPGetClientProtocol(host, loop)

    _, protocol = await loop\
        .create_connection(
            protocol_factory,
            host=host,
            port=port)
    return await protocol.get_response()


async def p82():
    loop = asyncio.get_running_loop()
    result = await make_request('www.sohu.com', 80, loop)
    logger.info(f'Result: {result}')


if __name__ == '__main__':
    asyncio.run(p82())
