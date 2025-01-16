import socket
import sys
from datetime import datetime
import pyfiglet
from concurrent.futures import ThreadPoolExecutor
import threading

print_lock = threading.Lock()

scanned_ports = set()

total_ports = 65535

def scan_port(target_ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.1)
            result = s.connect_ex((target_ip, port))
            with print_lock:
                scanned_ports.add(port)
                if result == 0:
                    print(f"\033[92mPort {port} is open\033[0m")
                else:
                    progress = len(scanned_ports) / total_ports * 100
                    print(f"Progress: {progress:.1f}%", end='\r')
    except Exception as e:
        pass

def main():
    
    ascii_banner = pyfiglet.figlet_format("ICED \n PORT SCANNER")
    print(ascii_banner)

    target = input("Enter the target to scan (e.g., IP address or hostname): ")

    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print("\n[!] Hostname Could Not Be Resolved!")
        sys.exit(1)

    print("-" * 50)
    print(f"Scanning Target: {target_ip}")
    print(f"Scanning started at: {datetime.now()}")
    print("-" * 50)

    try:
        with ThreadPoolExecutor(max_workers=500) as executor:
            for port in range(1, total_ports + 1):
                executor.submit(scan_port, target_ip, port)

        print("\n\nScan completed successfully!")
    except KeyboardInterrupt:
        print("\n[!] Scan terminated by user")
        sys.exit(0)
    except socket.error:
        print("\n[!] Server not responding!")
        sys.exit(0)

if __name__ == "__main__":
    main()
