import scapy.all
import socket
import threading
from queue import Queue
from scapy.layers.l2 import ARP, Ether

# Function to discover live hosts in the subnet using ARP
def discover_hosts(subnet):
    print(f"Discovering hosts in the subnet: {subnet}")
    arp = ARP(pdst=subnet)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    result = scapy.all.srp(packet, timeout=2, verbose=False)[0]

    live_hosts = []
    for sent, received in result:
        live_hosts.append(received.psrc)  # Store the IP address of the live host

    return live_hosts

# Function to scan a single port
def portscan(ip, port, results):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)  # Set timeout for connection attempts
        result = sock.connect_ex((ip, port))  # Try to connect to the port
        if result == 0:  # If connection was successful
            results.append(port)

# Worker function for threads
def worker(queue, ip, results):
    while not queue.empty():
        port = queue.get()
        portscan(ip, port, results)
        queue.task_done()

# Main function to scan ports on discovered hosts
def scan_ports(live_hosts):
    for ip in live_hosts:
        open_ports = []
        queue = Queue()

        # Add common ports to the queue (1-1024)
        for port in range(1, 1025):  # Change this range as needed
            queue.put(port)

        # Create and start threads
        threads = []
        for _ in range(200):  # Increased number of threads
            thread = threading.Thread(target=worker, args=(queue, ip, open_ports))
            thread.start()
            threads.append(thread)

        # Wait for all tasks in the queue to be completed
        queue.join()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        if open_ports:
            print(f"Open ports on {ip}: {open_ports}")
        else:
            print(f"No open ports found on {ip}.")

# Main entry point of the script
def main():
    target_subnet = input("Enter your subnet (e.g., 192.168.1.0/24): ")

    try:
        live_hosts = discover_hosts(target_subnet)

        if live_hosts:
            print(f"Live hosts found: {live_hosts}")
            scan_ports(live_hosts)
        else:
            print("No live hosts found in the specified subnet.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()