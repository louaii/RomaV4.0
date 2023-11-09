import platform
import netifaces
import subprocess
import asyncio
from scapy.all import conf
from check_local import get_private_ip

ip = str(get_private_ip())
conf.use_pcap = True
conf.sniff_promisc = True


def get_subnet_mask():
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        addresses = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addresses:
            for info in addresses[netifaces.AF_INET]:
                if info.get('addr') == get_private_ip():
                    subnet_mask = info.get('netmask')
                    return subnet_mask
    return None

def subnet_mask():
    try:
        subnet_octets = get_subnet_mask().split('.')
        binary_mask = "".join(format(int(octet), '08b') for octet in subnet_octets)
        prefix_length = binary_mask.count('1')
        return prefix_length
    except Exception as e:
        print(f"Error: {e}")
        return None


subnet = subnet_mask()

def ping_host(host):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", "-W", "2", host]  
    try:
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def scan_hosts(hosts):
    alive_hosts = []
    loop = asyncio.get_event_loop()
    tasks = [loop.run_in_executor(None, ping_host, host) for host in hosts]
    results = loop.run_until_complete(asyncio.gather(*tasks))
    for i in range(len(hosts)):
        if results[i]:
            alive_hosts.append(hosts[i])
    return alive_hosts

def ip_range(ip, subnet):
    host_bits = 32 - subnet
    num_hosts = 2 ** host_bits - 2  
    network_prefix = '.'.join(ip.split('.')[:4 - host_bits // 8])
    return [f"{network_prefix}.{i}" for i in range(1, num_hosts + 1)]

def icmp_scan1():
    hosts = ip_range(ip, subnet)
    return scan_hosts(hosts)

if __name__ == "__main__":
    print("All Alive Hosts:", icmp_scan1())
