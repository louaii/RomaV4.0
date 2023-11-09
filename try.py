from router_login import _username, _password
import requests
from bs4 import BeautifulSoup
from check_local import get_gateway
from manuf import manuf

router = get_gateway()
username = _username()
password = _password()
found = False

def get_mac_vendor(mac_address):
    api_url = f"https://api.macvendors.com/{mac_address}"
    response = requests.get(api_url)
    if response.status_code == 200:
        found = True
        return response.text.strip()
    else:
        parser = manuf.MacParser()
        vendor = parser.get_manuf(mac_address)
        if vendor:
            found = True
            return vendor
        elif found == False:
            mac_prefix = mac_address.lower()[:8]
            with open('mac_list.txt', 'r') as file:
                mac_vendor_list = [line.strip().split(' / ') for line in file]
            for line in mac_vendor_list:
                if mac_prefix == line[0]:
                    return line[1]
        else:
            return "Vendor not found"

try:
    url = f"http://{router}/dhcpclients.htm"
    response = requests.get(url, auth=(username, password), verify=False)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        form = soup.find("form", attrs={"name": "status"})
        if form is not None:
            table = form.find("table", attrs={"class": "formlisting"})
            if table is not None:
                rows = table.find_all("tr")[1:] 
                for row in rows:
                    cols = row.find_all('td')
                    hostname = cols[0].text.strip()
                    ip_address = cols[1].text.strip()
                    mac_address = cols[2].text.strip()
                    mac_vendor = get_mac_vendor(mac_address)
                    print(f'Host: {hostname}\nIP address: {ip_address}\nMac Address: {mac_address}\nMac Vendor: {mac_vendor}\n')
except:
    try:
        url = f"http://{router}/dhcpclients.htm"
        response = requests.get(url, auth=(username, password), verify=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            form = soup.find("form", attrs={"name": "status"})
            if form is not None:
                table = form.find("table", attrs={"class": "formlisting"})
                if table is not None:
                    rows = table.find_all("tr")[1:] 
                    for row in rows:
                        cols = row.find_all('td')
                        hostname = cols[0].text.strip()
                        ip_address = cols[1].text.strip()
                        mac_address = cols[2].text.strip()
                        print(f'Host: {hostname}\nIP address: {ip_address}\nMac Address: {mac_address}\n')
    except Exception as x:
        print(x)
        print(f"Error: {response.status_code}")
        print(response.content)     