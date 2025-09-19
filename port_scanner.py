#!/usr/bin/env python3

import socket
import threading
import argparse
from queue import Queue
import time
from termcolor import colored
import pyfiglet

print_lock = threading.Lock()

def create_banner():
    """Creates a cool ASCII art banner."""
    banner = pyfiglet.figlet_format("Port-Scanner", font="slant")
    print(colored(banner, 'cyan'))
    print(colored("-" * 50, 'cyan'))
    print(colored("          A multithreaded port scanner", 'cyan'))
    print(colored("-" * 50, 'cyan'))
    print()

def get_service_name(port):
    """Tries to get the common service name for a given port."""
    try:
        return socket.getservbyport(port)
    except OSError:
        return "Unknown"

def scan_port(target_ip, port, timeout):
    """
    Scans a single port on the target IP.
    Returns True if the port is open, False otherwise.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(timeout)
        result = s.connect_ex((target_ip, port))
        
        if result == 0:
            banner = ""
            try:
                s.send(b'HEAD / HTTP/1.0\r\n\r\n') 
                banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
            except:
                pass 

            service_name = get_service_name(port)

            with print_lock:
                print(colored(f"[+] Port {port:<5} is OPEN", 'green'), end='')
                print(colored(f"  Service: {service_name:<15}", 'yellow'), end='')
                if banner:
                    print(colored(f"  Banner: {banner.splitlines()[0]}", 'white'))
                else:
                    print() 
            s.close()

    except KeyboardInterrupt:
        print(colored("\n[!] Exiting program.", 'red'))
        exit()
    except socket.error:
        print(colored(f"[!] Couldn't connect to server: {target_ip}", 'red'))
        exit()

def worker(q, target_ip, timeout):
    """The worker thread function. Gets a port from the queue and scans it."""
    while not q.empty():
        port = q.get()
        scan_port(target_ip, port, timeout)
        q.task_done()

def parse_ports(port_string):
    """Parses port string like '1-100' or '80,443' into a list of integers."""
    ports = []
    if '-' in port_string:
        try:
            start, end = map(int, port_string.split('-'))
            if 0 < start <= end <= 65535:
                ports.extend(range(start, end + 1))
            else:
                raise ValueError
        except ValueError:
            print(colored(f"[!] Invalid port range: {port_string}", 'red'))
            exit()
    elif ',' in port_string:
        try:
            ports = [int(p) for p in port_string.split(',') if 0 < int(p) <= 65535]
        except ValueError:
            print(colored(f"[!] Invalid port list: {port_string}", 'red'))
            exit()
    else:
        try:
            port_num = int(port_string)
            if 0 < port_num <= 65535:
                ports.append(port_num)
            else:
                raise ValueError
        except ValueError:
            print(colored(f"[!] Invalid port number: {port_string}", 'red'))
            exit()
    return list(set(ports)) # Return unique ports

def main():
    parser = argparse.ArgumentParser(description="Advanced Port Scanner")
    parser.add_argument("target", help="The target IP address or hostname to scan.")
    parser.add_argument("-p", "--ports", default="1-1024", help="Port range to scan (e.g., 1-1024, 80,443).")
    parser.add_argument("-t", "--threads", type=int, default=50, help="Number of threads to use.")
    parser.add_argument("-T", "--timeout", type=float, default=0.5, help="Connection timeout in seconds.")
    
    args = parser.parse_args()

    target_host = args.target
    num_threads = args.threads
    timeout = args.timeout

    create_banner()
    
    try:
        target_ip = socket.gethostbyname(target_host)
        print(f"[*] Scanning Target: {target_host} ({target_ip})")
    except socket.gaierror:
        print(colored(f"[!] Hostname could not be resolved: {target_host}", 'red'))
        return

    ports_to_scan = parse_ports(args.ports)
    if not ports_to_scan:
        print(colored("[!] No valid ports to scan.", 'red'))
        return

    print(f"[*] Ports to Scan: {len(ports_to_scan)} | Threads: {num_threads} | Timeout: {timeout}s\n")

    q = Queue()
    for port in ports_to_scan:
        q.put(port)
        
    start_time = time.time()
    for _ in range(num_threads):
        thread = threading.Thread(target=worker, args=(q, target_ip, timeout))
        thread.daemon = True 
        thread.start()

    q.join()

   
    end_time = time.time()

    print(colored(f"\n[*] Scan completed in {end_time - start_time:.2f} seconds.", 'cyan'))

if __name__ == "__main__":
    main()
