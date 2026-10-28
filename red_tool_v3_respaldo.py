#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HERRAMIENTA DE DIAGNÓSTICO Y SOPORTE DE RED v4.0
Optimizada para Entornos Cloud, IT Support y Termux
"""

import socket
import os
import sys
import time
import json
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor

COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 8080, 8443]

def banner():
    print("\033[1;36m" + "="*60)
    print("      SUITE DE DIAGNÓSTICO Y SOPORTE TÉCNICO v4.0")
    print("           Perfil: IT Support & Cloud Operations")
    print("="*60 + "\033[0m")

def obtener_ip_local():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_local = s.getsockname()[0]
        s.close()
        return ip_local
    except Exception:
        return "127.0.0.1"

def escanear_puerto(target_ip, port, timeout=1.5):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            banner_text = ""
            try:
                sock.send(b'HEAD / HTTP/1.0\r\n\r\n')
                respuesta = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                banner_text = respuesta.split('\n')[0] if respuesta else "Sin banner"
            except Exception:
                banner_text = "No disponible"
            sock.close()
            return port, True, banner_text
        sock.close()
        return port, False, ""
    except Exception:
        return port, False, ""

def modulo_escaneo_puertos():
    print("\n\033[1;33m--- [1] Escaneo y Auditoría de Puertos (Multihilo) ---\033[0m")
    target = input("Ingresa la IP o Dominio objetivo (ej. 127.0.0.1 o google.com): ").strip()
    if not target:
        target = "127.0.0.1"
    
    try:
        target_ip = socket.gethostbyname(target)
        print(f"\n[+] Objetivo: {target} ({target_ip})")
        print("[+] Ejecutando escaneo concurrente...\n")
        
        resultados = []
        inicio = time.time()
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(escanear_puerto, target_ip, port) for port in COMMON_PORTS]
            for future in futures:
                port, abierto, banner_info = future.result()
                if abierto:
                    print(f"  \033[1;32m[ ABIERTO ]\033[0m Puerto {port:<5} | Info: {banner_info[:40]}")
                    resultados.append({"puerto": port, "estado": "abierto", "info": banner_info})
                else:
                    print(f"  \033[1;31m[ CERRADO ]\033[0m Puerto {port:<5}")
        
        duracion = round(time.time() - inicio, 2)
        print(f"\n[+] Escaneo finalizado en {duracion} segundos.")
        
        guardar = input("\n¿Guardar resultados en JSON? (s/n): ").strip().lower()
        if guardar == 's':
            guardar_reporte_json({"objetivo": target, "ip": target_ip, "puertos": resultados})
            
    except socket.gaierror:
        print("\033[1;31m[-] Error: No se pudo resolver el nombre de host.\033[0m")

def modulo_diagnostico_web():
    print("\n\033[1;33m--- [2] Inspección de Encabezados HTTP/HTTPS de Seguridad ---\033[0m")
    url = input("Ingresa la URL (ej. https://ejemplo.com): ").strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
        
    print(f"\n[+] Conectando a {url}...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'CloudSupportBot/4.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            headers = response.info()
            print(f"[+] Estado HTTP: \033[1;32m{response.status} {response.reason}\033[0m\n")
            print("--- Cabeceras Clave de Seguridad ---")
            
            claves = ['Server', 'Date', 'Content-Type', 'Strict-Transport-Security', 'X-Frame-Options', 'Content-Security-Policy']
            for clave in claves:
                val = headers.get(clave, "\033[1;31mNo configurado\033[0m")
                print(f"  * {clave:<28}: {val}")
    except urllib.error.HTTPError as e:
        print(f"\033[1;31m[-] Error HTTP {e.code}: {e.reason}\033[0m")
    except Exception as e:
        print(f"\033[1;31m[-] Error de conexión: {str(e)}\033[0m")

def modulo_resolucion_dns():
    print("\n\033[1;33m--- [3] Resolución y Consulta de Registros DNS ---\033[0m")
    dominio = input("Ingresa el dominio a consultar (ej. github.com): ").strip()
    if not dominio:
        print("[-] Dominio no válido.")
        return
    
    print(f"\n[+] Consultando registros para: {dominio}")
    try:
        # Obtener información de direcciones IP asociadas
        info_dns = socket.gethostbyname_ex(dominio)
        print(f"  * Nombre Oficial : {info_dns[0]}")
        print(f"  * Alias (CNAME)  : {info_dns[1] if info_dns[1] else 'Ninguno'}")
        print(f"  * Direcciones IP :")
        for ip in info_dns[2]:
            print(f"    -> {ip}")
    except socket.gaierror:
        print("\033[1;31m[-] Error: No se pudo resolver el dominio especificado.\033[0m")

def modulo_latencia_cloud():
    print("\n\033[1;33m--- [4] Prueba de Latencia hacia Endpoints Clave ---\033[0m")
    destinos = {
        "Google DNS": "8.8.8.8",
        "Cloudflare DNS": "1.1.1.1",
        "Gateway Local": obtener_ip_local()
    }
    
    print("[+] Midiendo tiempos de respuesta TCP (Port 53 / 443)...\n")
    for nombre, ip in destinos.items():
        try:
            inicio = time.time()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2.0)
            s.connect((ip, 53 if ip != obtener_ip_local() else 80))
            s.close()
            latencia = round((time.time() - inicio) * 1000, 2)
            print(f"  * {nombre:<16} ({ip}) -> \033[1;32m{latencia} ms\033[0m")
        except Exception:
            print(f"  * {nombre:<16} ({ip}) -> \033[1;31mSin respuesta / Timeout\033[0m")

def modulo_generador_tickets():
    print("\n\033[1;33m--- [5] Generador de Reportes de Incidencias (Soporte TI) ---\033[0m")
    print("Completa los datos para registrar el ticket de soporte técnico:\n")
    
    incidente = input("Título o síntoma del incidente: ").strip()
    afectado = input("Dispositivo / IP / Host afectado: ").strip()
    diagnostico = input("Diagnóstico preliminar / Acciones tomadas: ").strip()
    severidade = input("Severidad (Baja / Media / Crítica): ").strip()
    
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    nombre_archivo = f"ticket_soporte_{time.strftime('%Y%m%d_%H%M%S')}.md"
    
    contenido_markdown = f"""# REPORTE DE INCIDENTE TÉCNICO (SOPORTE TI)
* **Fecha y Hora:** {timestamp}
* **Severidad:** {severidade}
* **Objetivo / Host Afectado:** {afectado}

## 1. Descripción del Problema
{incidente}

## 2. Acciones de Diagnóstico y Mitigación
{diagnostico}

## 3. Estado Actual
* **Resolución:** Documentado y escalado para revisión operativa.
* **Generado por:** Automatización móvil (Termux / Python Tool v4.0)
"""
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write(contenido_markdown)
        print(f"\n\033[1;32m[+] Ticket generado exitosamente como: {nombre_archivo}\033[0m")
    except Exception as e:
        print(f"\033[1;31m[-] Error al crear el ticket: {str(e)}\033[0m")

def modulo_monitor_sistema():
    print("\n\033[1;33m--- [6] Monitor de Recursos y Red Local ---\033[0m")
    print(f"[+] IP Local Asignada: \033[1;32m{obtener_ip_local()}\033[0m")
    print(f"[+] Marca de tiempo   : {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    print("--- Uso de Almacenamiento ---")
    os.system("df -h /data/data/com.termux/files/home 2>/dev/null || df -h .")
    print("\n--- Estado de Memoria ---")
    os.system("free -m 2>/dev/null || cat /proc/meminfo | head -n 4")

def guardar_reporte_json(datos):
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    nombre_archivo = f"reporte_red_{timestamp}.json"
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
        print(f"\033[1;32m[+] Reporte JSON guardado en: {nombre_archivo}\033[0m")
    except Exception as e:
        print(f"\033[1;31m[-] Error: {str(e)}\033[0m")

def menu_principal():
    while True:
        banner()
        print(" 1. Escaneo y Auditoría de Puertos (Multihilo)")
        print(" 2. Inspección de Encabezados HTTP/HTTPS")
        print(" 3. Resolución y Consulta de Registros DNS")
        print(" 4. Prueba de Latencia hacia Endpoints Cloud")
        print(" 5. Generador de Reportes de Incidencias (Tickets TI)")
        print(" 6. Monitor de Recursos del Sistema")
        print(" 7. Salir")
        print("="*60)
        
        opcion = input("Selecciona una opción (1-7): ").strip()
        
        if opcion == '1':
            modulo_escaneo_puertos()
        elif opcion == '2':
            modulo_diagnostico_web()
        elif opcion == '3':
            modulo_resolucion_dns()
        elif opcion == '4':
            modulo_latencia_cloud()
        elif opcion == '5':
            modulo_generador_tickets()
        elif opcion == '6':
            modulo_monitor_sistema()
        elif opcion == '7':
            print("\n¡Cerrando la suite de soporte. Buen trabajo!\n")
            sys.exit(0)
        else:
            print("\n\033[1;31m[-] Opción inválida. Intenta nuevamente.\033[0m")
            
        input("\nPresiona [Enter] para volver al menú...")
        os.system("clear")

if __name__ == "__main__":
    try:
        os.system("clear")
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n[-] Sesión finalizada por el usuario.\n")
        sys.exit(0)


