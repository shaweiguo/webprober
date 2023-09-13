import asyncio
import aiohttp
import ipaddress
from urllib.parse import urlparse


async def check_web_app(semaphore, url):
    async with semaphore:
        print(url)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    # if response.status == 200:
                    #     print(f"{url} is up and running")
                    #     return {
                    #         'status': response.status,
                    #         'url': url
                    #     }
                    # else:
                    #     print(f"{url} is down")
                    return {
                        'status': response.status,
                        'url': url
                    }
        except aiohttp.ClientError as err:
            # print(err)
            return {
                'status': 0,
                'url': url
            }

def extract_url(url):
    parsed_url = urlparse(url)
    ip = parsed_url.hostname
    port = parsed_url.port
    return ip, port

async def scan_network(nums, subnet):
    ports = set()
    ports.add(80)
    ports.add(443)
    for i in range(1025, 65535):
        ports.add(i)
    for ip in ipaddress.IPv4Network(subnet):
        tasks = []
        semaphore = asyncio.Semaphore(nums)
        for port in ports:
            url = f"http://{ip}:{port}"
            tasks.append(check_web_app(semaphore, url))
        results = await asyncio.gather(*tasks)
        for i, result in enumerate(results):
            if result['status'] == 200:
                url = result['url']
                ip, port = extract_url(url)
                print(f"Web application found at {ip}:{port}")