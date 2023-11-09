from arp import arp_scan
from icmp1 import icmp_scan1
from icmp2 import icmp_scan2

icmp_host1 = icmp_scan1()
icmp_host2 = icmp_scan2()

def combine_hosts():
    arp_host = arp_scan()
    hosts = list(set(arp_host + icmp_host1 + icmp_host2))
    hosts.sort()
    return hosts

def icmp_scan():
    hosts = list(set(icmp_host1 + icmp_host2))
    hosts.sort()
    return hosts

def get_hosts():
    hosts = combine_hosts()
    return hosts

if __name__ == "__main__":
    print("icmp:" , icmp_scan())
    print("arp:", arp_scan())
    print("All Alive Hosts:", get_hosts())
