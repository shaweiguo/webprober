# import subprocess
# import threading
# import ipaddress

# # 定义要扫描的网段
# network = '192.168.6.0/24'

# # 定义保存结果的文件名
# output_file = 'web_servers.txt'

# # 定义nmap命令及参数
# nmap_command = ['nmap', '-p', '80,443', '--open', '-oG', '-']

# # 用于保存扫描结果的列表
# web_servers = []

# # 定义一个函数，用于执行nmap扫描
# def scan_ip(ip):
#     # 构造nmap命令
#     command = nmap_command + [str(ip)]
#     # 执行nmap命令并获取输出
#     output = subprocess.check_output(command, universal_newlines=True)
#     # 解析nmap输出，查找开放的http或https端口
#     if '80/open' in output or '443/open' in output:
#         web_servers.append(str(ip))

# # 构造IP地址对象列表
# ips = [ipaddress.ip_address(str(ip)) for ip in ipaddress.IPv4Network(network)]

# # 创建多个线程并启动扫描任务
# threads = []
# for ip in ips:
#     thread = threading.Thread(target=scan_ip, args=(ip,))
#     threads.append(thread)
#     thread.start()

# # 等待所有线程执行完毕
# for thread in threads:
#     thread.join()

# # 将结果保存到文件中
# with open(output_file, 'w') as f:
#     f.write('\n'.join(web_servers))
import subprocess
import json
from multiprocessing import Pool

def scan_port(ip):
    result = {}
    try:
        # 调用nmap命令扫描指定IP的所有端口
        output = subprocess.check_output(["nmap", "-p-", ip])
        # 解析扫描结果
        lines = output.decode().split("\n")
        for line in lines:
            if line.startswith("PORT"):
                continue
            if line.strip() == "":
                break
            port_info = line.split("/")
            port = port_info[0].strip()
            protocol = port_info[1].strip()
            service = port_info[2].strip()
            result[port] = {
                "protocol": protocol,
                "service": service
            }
    except subprocess.CalledProcessError:
        pass
    
    return ip, result

def main():
    # 指定要扫描的网段
    network = "192.168.0.0/24"
    ips = [f"{network[:-3]}{i}" for i in range(1, 255)]
    
    # 使用进程池实现高并发多进程
    with Pool(4) as pool:
        results = pool.map_async(scan_port, ips)
    
    # 将扫描结果保存为JSON文件
    output = {}
    for ip, result in results.get():
        if result:
            output[ip] = result
    
    with open("scan_result.json", "w") as file:
        json.dump(output, file, indent=4)

if __name__ == "__main__":
    main()
