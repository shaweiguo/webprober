import socket
import concurrent.futures
import asyncio
import aiohttp
import socket
import ipaddress
from concurrent.futures import ProcessPoolExecutor
import subprocess
from bs4 import BeautifulSoup

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

def check_web_service_concurrent(ip, ports, max_workers):
    # 创建线程池
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交任务并获取Future对象列表
        futures = [executor.submit(check_web_service, ip, port) for port in ports]
        # 等待所有任务完成并获取结果列表
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    # 返回结果
    return results

async def get_webapp_info(ip, port):
    try:
        async with aiohttp.ClientSession() as session:
            url = f"http://{ip}:{port}"
            async with session.get(url) as response:
                if response.status == 200:
                    print(f"HTTP service found at {ip}:{port}")
                    html = await response.text()
                    soup = BeautifulSoup(html, "html.parser")
                    title = soup.title.string
                    charset = soup.meta.get('charset')
                    print(f"Title is {title}, chartset is {charset}")
            url = f"https://{ip}:{port}"
            async with session.get(url) as response:
                if response.status == 200:
                    print(f"HTTPS service found at {ip}:{port}")
    except (aiohttp.ClientError, socket.gaierror):
        pass

# 示例用法
ip = '192.168.6.2'
ports = set()
ports.update([80, 443])
ports.update(range(1025, 65535))
max_workers = 2

scan_results = []
results = check_web_service_concurrent(ip, ports, max_workers)
for i, port in enumerate(ports):
    if results[i]:
        print(f'The {ip}:{port} provides web service.')
        # result = await get_webapp_info(ip, port)
        scan_results.append({'ip': ip, 'port': port, 'status': results[i]})
    # else:
    #     print(f'The {ip}:{port} does not provide web service.')
