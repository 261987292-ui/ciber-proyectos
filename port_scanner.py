import socket
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

def escanear_puerto(host, puerto):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.4)
        resultado = s.connect_ex((host, puerto))
        if resultado == 0:
            banner = "Servicio activo"
            try:
                # Intentamos solicitar información básica al puerto para capturar el banner
                s.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
                respuesta = s.recv(512).decode('utf-8', errors='ignore').split('\n')
                if respuesta:
                    banner = respuesta[0].strip()
            except Exception:
                pass
            
            print(f" [!] Puerto {puerto}/TCP -> ABIERTO [{banner}]")
        s.close()
    except Exception:
        pass

def escanear_objetivo(host):
    print(f"\n[+] Iniciando auditoría avanzada en: {host}")
    print(f"[+] Hora de inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)
    
    with ThreadPoolExecutor(max_workers=100) as executor:
        for puerto in range(1, 1025):
            executor.submit(escanear_puerto, host, puerto)
            
    print("=" * 65)
    print(f"[+] Auditoría finalizada en {host}.")

if __name__ == "__main__":
    host_destino = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    escanear_objetivo(host_destino)
