import socket

def check_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result == 0

print("Scanning for MySQL ports...")
ports = [3306, 3307, 3308, 8889]
found = False
for p in ports:
    if check_port(p):
        print(f"SUCCESS: Found something running on port {p}")
        found = True
    else:
        print(f"Port {p} is closed.")

if not found:
    print("No common MySQL ports are open. XAMPP MySQL is likely NOT running.")
