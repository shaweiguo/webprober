import subprocess

ip_address = "192.168.0.1"
port = 80

result = subprocess.run(["rustscan", ip_address, "--port", str(port)], capture_output=True, text=True)
print(result)