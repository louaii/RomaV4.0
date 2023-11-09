import importlib
import subprocess
import os
import socket

def check_dependencies(dependencies):
    missing_dependencies = []
    for dependency in dependencies:
        try:
            importlib.import_module(dependency)
        except ImportError:
            missing_dependencies.append(dependency)
    return missing_dependencies

def install_dependencies(dependencies):
    for dependency in dependencies:
        try:
            with open(os.devnull, 'w') as devnull:
                subprocess.check_call(['pip', 'install', dependency], stdout=devnull, stderr=devnull)
        except Exception as e:
            print(f"\033[1;31m+ !Error installing {dependency}\033[0m")
            break

def check_internet_connection():
    try:
        socket.create_connection(("8.8.8.8", 80))
        return True
    except OSError:
        return False

required_dependencies = [    
    'sys',
    'getpass',
    'subprocess',
    'socket',
    'os',
    'importlib',
    'python-arpreq', 
    'ipaddress', 
    'argparse', 
    'pcapy', 
    'pyshark', 
    'dpkt', 
    'GeoIP2', 
    'psutil', 
    'netmiko',
    'pexpect', 
    'pynacl', 
    'pydim', 
    'netifaces',
    'requests',
    'mac-vendor-lookup',
    'scapy',
    'python-nmap',
    'paramiko',
    'concurrent.futures',
    'pysnmp.hlapi'
]

missing_dependencies = check_dependencies(required_dependencies)
if missing_dependencies:
    install_dependencies(missing_dependencies)
 