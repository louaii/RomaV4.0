import platform
import subprocess
import asyncio
import netifaces
from scapy.all import conf
from check_local import get_private_ip

conf.use_pcap = True
conf.sniff_promisc = True

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


def icmp_scan2():
    ip = get_private_ip()
    subnet = get_subnet_mask()

    if subnet == "255.0.0.0":
        network_prefix = ip.split(".")[0]
        hosts = [f"{network_prefix}.{i}.{j}.{k}" for i in range(1, 256) for j in range(1, 256) for k in range(1, 256)]
    elif subnet == "255.255.0.0":
        network_prefix = ip.split(".")[0] + "." + ip.split(".")[1]
        hosts = [f"{network_prefix}.{i}.{j}" for i in range(1, 256) for j in range(1, 256)]
    else:
        network_prefix = ip.split(".")[0] + "." + ip.split(".")[1] + "." + ip.split(".")[2]
        hosts = [f"{network_prefix}.{i}" for i in range(1, 256)]

    return scan_hosts(hosts)

if __name__ == "__main__":
    print("All Alive Hosts:", icmp_scan2())
