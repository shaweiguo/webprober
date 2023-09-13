import subprocess
import ipaddress

def ping(ip):
    try:
        output = subprocess.check_output(['ping', '-c', '1', '-W', '1', str(ip)], stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def scan_network(network):
    ip_generator = (ip for ip in ipaddress.IPv4Network(network).hosts())
    for ip in ip_generator:
        if ping(ip):
            print(f"{ip} is up")
        else:
            print(f"{ip} is down")

scan_network("192.168.6.0/24")
