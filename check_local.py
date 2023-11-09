import psutil
import netifaces
import requests
from mac_vendor_lookup import MacLookup
import socket
import getpass
import netaddr

def get_private_ip():
    interfaces = psutil.net_if_addrs()
    for interface in interfaces.values():
        for address in interface:
            if address.family == socket.AddressFamily.AF_INET and not address.address.startswith("127."):
                return address.address

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org', timeout=5)
        response.raise_for_status()
        return response.text.strip()
    except requests.exceptions.ReadTimeout:
        try:
            response = requests.get('https://api.ipify.org', timeout=15)
            response.raise_for_status()
            return response.text.strip()
        except requests.exceptions.RequestException as e:
            print(f"Warning Error: {e}")
            return 'N/A'
    except requests.exceptions.RequestException as e:
        print(f"Warning Error: {e}")
        return 'N/A'

def get_mac_vendor(mac_address):
    return MacLookup().lookup(mac_address)

def get_mac_address():
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        if 'eth' in interface or 'wlan' in interface:
            mac_address = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
            return mac_address

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


def get_gateway():
    gateways = netifaces.gateways()
    default_gateway = gateways['default']
    if netifaces.AF_INET in default_gateway:
        default_gateway_ip = default_gateway[netifaces.AF_INET][0]
        default_gateway_interface = default_gateway[netifaces.AF_INET][1]
        subnet_mask = get_subnet_mask()
        if subnet_mask is not None:
            network_str = f"{get_private_ip()}/{subnet_mask}"
            network = netaddr.IPNetwork(network_str)
            if netaddr.IPAddress(default_gateway_ip) in network:
                return default_gateway_ip

    return 'N/A'



def subnet_mask():
    try:
        subnet_octets = get_subnet_mask().split('.')
        binary_mask = "".join(format(int(octet), '08b') for octet in subnet_octets)
        prefix_length = binary_mask.count('1')
        return f"/{prefix_length}"
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_username():
    return getpass.getuser()

def get_location(public_ip):
    url = f"http://ip-api.com/json/{public_ip}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('country', 'N/A'), data.get('regionName', 'N/A'), data.get('city', 'N/A')
    else:
        return 'N/A', 'N/A', 'N/A'


user = get_username()
private_ip = get_private_ip()
public_ip = get_public_ip()
mac_address = get_mac_address()
mac_vendor = get_mac_vendor(mac_address)
country, region, city = get_location(public_ip)
mask = subnet_mask()
gateway = get_gateway()
subnet = get_subnet_mask()
def print_local():
    print()
    if city != 'N/A' and region != 'N/A' and country != 'N/A':
        print(f"{user}: \033[1;32m{city}, {region}, {country}\033[0m")
    else:
        print(f"{user}:")
    print(f".Gateway: \033[1;32m{gateway}\033[0m")
    print(f".Private IP: \033[1;32m{private_ip}{mask}\033[0m")
    print(f".Public IP: \033[1;32m{public_ip}\033[0m")
    print(f".MAC Address: \033[1;32m{mac_address}\033[0m")
    print(f".Manufacturer: \033[1;32m{mac_vendor}\033[0m")
    print(f".Subnet Mask: \033[1;32m{subnet}\033[0m")