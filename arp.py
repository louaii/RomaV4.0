import socket
from scapy.all import ARP, Ether, srp

def get_local_ip_address():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(('8.8.8.8', 80))
        local_ip_address = sock.getsockname()[0]
    except socket.error:
        local_ip_address = socket.gethostbyname(socket.gethostname())
    finally:
        sock.close()
    return local_ip_address

def arp_scan():
    local_ip_address = get_local_ip_address()
    network_address = local_ip_address[:local_ip_address.rfind('.')] + '.0/24'
    arp = ARP(pdst=network_address)
    ether = Ether(dst='ff:ff:ff:ff:ff:ff')
    packet = ether/arp
    try:
        result = srp(packet, timeout=3, verbose=0, iface="eth0")[0]
        alive_hosts = [received.psrc for sent, received in result]
    except Exception as e:
        print(f"Error: {e}")
        alive_hosts = []

    return alive_hosts

if __name__ == "__main__":
    print("All Alive Hosts:", arp_scan())
