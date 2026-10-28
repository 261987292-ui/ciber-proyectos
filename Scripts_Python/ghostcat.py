import sys
import socket

def check_ajp(host, port):
    print(f"[*] Verificando servicio AJP en {host}:{port}...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4)
        s.connect((host, port))
        print("[+] ¡Conexión exitosa! El puerto AJP está activo y accesible en la red.")
        s.close()
    except Exception as e:
        print(f"[-] Error al conectar con el puerto AJP: {e}")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "192.168.0.47"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8009
    check_ajp(target, port)
