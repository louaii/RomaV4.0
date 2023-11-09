from router_login import _username, _password
import requests
from bs4 import BeautifulSoup
from check_local import get_gateway

router = get_gateway()
username = _username()
password = _password()


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