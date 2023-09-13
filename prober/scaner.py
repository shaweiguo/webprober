import asyncio
import aiohttp
import socket
import ipaddress
from concurrent.futures import ProcessPoolExecutor
import subprocess
from bs4 import BeautifulSoup


async def scan_port(ip, port):
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

async def scan_ip(ip):
    tasks = []
    for port in range(1, 65536):
        tasks.append(scan_port(str(ip), port))
    await asyncio.gather(*tasks)

def run_scan(ip, max_processes):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(scan_ip(ip))
    loop.close()

def ping(ip):
    try:
        output = subprocess.check_output(['ping', '-c', '1', '-W', '1', str(ip)], stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

async def scan_network(network, max_processes):
    ip_generator = (ip for ip in ipaddress.IPv4Network(network).hosts())
    with ProcessPoolExecutor(max_workers=max_processes) as executor:
        for ip in ip_generator:
            if ping(ip):
                executor.submit(run_scan, str(ip), max_processes)

asyncio.run(scan_network("192.168.6.0/24", max_processes=10))
