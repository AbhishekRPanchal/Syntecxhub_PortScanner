import socket
import threading
from datetime import datetime

# Lock for thread-safe printing
print_lock = threading.Lock()

# Function to log results into a file
def log(message):
    with open("scan_log.txt", "a") as f:
        f.write(f"{datetime.now()} - {message}\n")

# Safely get service name for known ports
def get_service_name(port):
    try:
        return socket.getservbyport(port)
    except:
        return "Unknown"

# Function to scan a single port
def scan_port(host, port, timeout=1):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)

        result = s.connect_ex((host, port))  # 0 = open
        service = get_service_name(port)

        with print_lock:
            if result == 0:
                print(f"[OPEN]   Port {port} ({service})")
                log(f"[OPEN] Port {port} ({service})")
            else:
                print(f"[CLOSED] Port {port} ({service})")
                log(f"[CLOSED] Port {port} ({service})")

        s.close()

    except Exception as e:
        log(f"[ERROR] Port {port} : {e}")

# Main scanner function
def run_scan():
    host = input("Enter target host (e.g., 192.168.1.1): ")
    start_port = int(input("Start port: "))
    end_port = int(input("End port: "))

    print(f"\nScanning {host} from port {start_port} to {end_port}...\n")
    log(f"--- New Scan Started for {host} ({start_port}-{end_port}) ---")

    threads = []

    # Create a thread for each port
    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(host, port))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    print("\nScan Complete!")
    log("--- Scan Completed ---\n")

if __name__ == "__main__":
    run_scan()
