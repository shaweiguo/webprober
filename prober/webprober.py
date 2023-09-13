from collections.abc import Callable, Iterable, Mapping
import threading
from typing import Any
import requests
import socket


def check_web_service(ip, port):
    try:
        # 创建套接字对象
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置超时时间
        s.settimeout(2)
        # 连接目标主机和端口
        s.connect((ip, port))
        # 发送HTTP请求
        s.send(b'GET / HTTP/1.1\r\nHost: ' + ip.encode() + b'\r\n\r\n')
        # 接收服务器响应
        response = s.recv(1024)
        # 判断响应是否包含HTTP头
        if b'HTTP/' in response:
            # 如果包含HTTP头，则说明提供web服务
            return True
        else:
            return False
    except:
        return False

class WebProber(threading.Thread):
    def __init__(self, ip, port) -> None:
        super().__init__(self)
        self.ip = ip
        self.port = port
        self.result = None
    
    def run(self):
        url = f'http://{self.ip}:{self.port}'
        res = requests.get(f'http://{self.ip}:{self.port}')
        self.result = f'{self.url}: {res.status_code} - {res.text}'
    
    def is_web(self):

