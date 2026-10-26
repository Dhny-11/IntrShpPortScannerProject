import socket
import re
from common_ports import ports_and_services

def get_open_ports(target, port_range, verbose=False):
    open_ports = []
    
    # Cek apakah target hanya berisi angka dan titik (indikasi format IP)
    is_ip = re.match(r"^\d+\.\d+\.\d+\.\d+$", target)
    
    ip = ""
    url = None

    if is_ip:
        # Validasi setiap angka (oktet) IP harus berada di rentang 0 - 255
        octets = target.split(".")
        if len(octets) != 4 or not all(o.isdigit() and 0 <= int(o) <= 255 for o in octets):
            return "Error: Invalid IP address"
        
        ip = target
        # Bungkus gethostbyaddr dengan try-except agar tidak error saat IP tidak punya hostname (Unknown host)
        try:
            url = socket.gethostbyaddr(ip)[0]
        except (socket.herror, socket.gaierror, socket.error):
            url = None
    else:
        # Jika input berupa URL / hostname
        try:
            ip = socket.gethostbyname(target)
            url = target
        except (socket.gaierror, socket.error):
            return "Error: Invalid hostname"

    # Pindai rentang port dari port_range[0] hingga port_range[1]
    for port in range(port_range[0], port_range[1] + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        
        if s.connect_ex((ip, port)) == 0:
            open_ports.append(port)
        s.close()

    # Kembalikan list jika bukan mode verbose
    if not verbose:
        return open_ports

    # Format output string untuk mode verbose
    if url:
        header = f"Open ports for {url} ({ip})\n"
    else:
        header = f"Open ports for {ip}\n"
        
    header += "PORT     SERVICE"
    
    lines = [header]
    for port in open_ports:
        service_name = ports_and_services.get(port, "")
        lines.append(f"{port:<9}{service_name}")

    return "\n".join(lines)