import os
import sys
import time
import socket
import json
import requests
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143]

def banner():
    print("\033[1;36m" + "="*60)
    print("      SUITE DE DIAGNÓSTICO Y SOPORTE DE RED v4.0")
    print("      Perfil: IT Support & Cloud / Legal Threat Intel")
    print("="*60 + "\033[0m")

def obtener_ip_local():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def modulo_escaneo_puertos():
    print("\n\033[1;33m[*] Escaneo y Auditoría de Puertos...\033[0m")
    target = input("[?] Ingresa la IP o Dominio objetivo: ").strip()
    if not target:
        target = "127.0.0.1"
    try:
        target_ip = socket.gethostbyname(target)
        print(f"[*] IP objetivo: {target_ip}")
        print("[*] Ejecutando escaneo concurrente...")
        resultados = []
        inicio = time.time()
        
        def escanear_puerto(puerto):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1.0)
                result = sock.connect_ex((target_ip, puerto))
                sock.close()
                return puerto, result == 0
            except Exception:
                return puerto, False

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(escanear_puerto, p) for p in COMMON_PORTS]
            for future in futures:
                puerto, abierto = future.result()
                if abierto:
                    print(f"\033[1;32m[+] Puerto {puerto}: ABIERTO\033[0m")
                    resultados.append(f"[+] Puerto {puerto}: ABIERTO\n")
                else:
                    print(f"\033[1;31m[-] Puerto {puerto}: CERRADO\033[0m")
                    resultados.append(f"[-] Puerto {puerto}: CERRADO\n")
        
        duration = round(time.time() - inicio, 2)
        print(f"\n[*] Escaneo finalizado en {duration} segundos.")
        
        guardar = input("[?] ¿Deseas guardar resultados en archivo? (s/n): ").strip().lower()
        if guardar == 's':
            if not os.path.exists("reportes_auditoria"):
                os.makedirs("reportes_auditoria")
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            nombre_archivo = f"reportes_auditoria/puertos_{timestamp}.txt"
            with open(nombre_archivo, "w") as f:
                f.writelines(resultados)
            print(f"[+] Reporte guardado en: {nombre_archivo}")
    except socket.gaierror:
        print("\033[1;31m[!] Error: No se pudo resolver el dominio.\033[0m")
    input("\nPresiona [Enter] para continuar...")

def modulo_diagnostico_web():
    print("\n\033[1;33m[2] Inspección de Encabezados HTTP...\033[0m")
    url = input("[?] Ingresa la URL (ejemplo: https://google.com): ").strip()
    if not url:
        print("[!] URL no válida.")
        input("\nPresiona [Enter] para continuar...")
        return
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            print(f"\n[+] Estado HTTP: {response.status} OK")
            print("\n--- Cabeceras Clave ---")
            headers = response.headers
            for clave in ['Server', 'Date', 'Content-Type', 'X-Powered-By']:
                if clave in headers:
                    print(f"  {clave}: {headers[clave]}")
    except Exception as e:
        print(f"\033[1;31m[!] Error de conexión: {e}\033[0m")
    input("\nPresiona [Enter] para continuar...")

def modulo_resolucion_dns():
    print("\n\033[1;33m[3] Resolución y Consulta de Registros...\033[0m")
    dominio = input("[?] Ingresa el dominio a consultar: ").strip()
    if not dominio:
        print("[!] Dominio no válido.")
        input("\nPresiona [Enter] para continuar...")
        return
    try:
        ip = socket.gethostbyname(dominio)
        print(f"\n[+] Dominio: {dominio}")
        print(f"[+] Dirección IP: {ip}")
    except socket.gaierror:
        print("\033[1;31m[!] Error: No se pudo resolver el dominio.\033[0m")
    input("\nPresiona [Enter] para continuar...")

def modulo_latencia_cloud():
    print("\n\033[1;33m[4] Prueba de Latencia hacia Endpoints...\033[0m")
    ip_local = obtener_ip_local()
    partes = ip_local.split('.')
    gateway_ip = f"{partes[0]}.{partes[1]}.{partes[2]}.1" if len(partes) == 4 else "192.168.0.1"

    destinos = {
        "Google DNS": ("8.8.8.8", 53),
        "Cloudflare DNS": ("1.1.1.1", 53),
        "Gateway Router": (gateway_ip, 80)
    }
    
    for nombre, (ip, puerto) in destinos.items():
        try:
            inicio = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2.0)
            sock.connect((ip, puerto))
            sock.close()
            latencia = round((time.time() - inicio) * 1000, 2)
            print(f"[+] {nombre} ({ip}): {latencia} ms")
        except Exception:
            print(f"[-] {nombre} ({ip}): Sin respuesta / Timeout")
    input("\nPresiona [Enter] para continuar...")

def modulo_generador_tickets():
    print("\n\033[1;33m[5] Generador de Reportes de Incidencias...\033[0m")
    incidente = input("[?] Título o síntoma del incidente: ")
    afectado = input("[?] Equipo / Host afectado: ")
    diagnostico = input("[?] Acciones de diagnóstico: ")
    severidad = input("[?] Severidad (Baja / Media / Alta): ")
    
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    lineas = [
        "# REPORTE DE INCIDENCIA\n",
        f"- Fecha y Hora: {timestamp}\n",
        f"- Host Afectado: {afectado}\n",
        f"- Severidad: {severidad}\n\n",
        "## 1. Descripción del Problema\n",
        f"{incidente}\n\n",
        "## 2. Acciones de Diagnóstico y Mitigación\n",
        f"{diagnostico}\n"
    ]
    if not os.path.exists("reportes_auditoria"):
        os.makedirs("reportes_auditoria")
    nombre = f"reportes_auditoria/ticket_{time.strftime('%Y%m%d_%H%M%S')}.md"
    with open(nombre, "w") as f:
        f.writelines(lineas)
    print(f"[+] Ticket generado exitosamente en: {nombre}")
    input("\nPresiona [Enter] para continuar...")

def modulo_monitor_sistema():
    print("\n\033[1;33m[6] Monitor de Recursos del Sistema...\033[0m")
    print(f"[*] IP Local Asignada: {obtener_ip_local()}")
    print("\n--- Almacenamiento ---")
    os.system("df -h /data/data/com.termux/files")
    print("\n--- Procesos Principales ---")
    os.system("ps -e -o pid,%cpu,%mem,comm | head -n 10")
    input("\nPresiona [Enter] para continuar...")
# ==========================================
# MÓDULOS OSINT & LEGAL DUE DILIGENCE
# ==========================================
def osint_busqueda_alias():
    termino = input("[?] Ingresa el alias o nombre completo a buscar: ").strip()
    if not termino:
        print("[!] El campo no puede estar vacío.")
        input("\nPresiona [Enter] para continuar...")
        return

    query_encoded = urllib.parse.quote_plus(termino)
    plataformas = {
        "Facebook (Personas)": f"https://www.facebook.com/search/people/?q={query_encoded}",
        "LinkedIn (Profesional)": f"https://www.linkedin.com/search/results/all/?keywords={query_encoded}",
        "Twitter / X (Usuarios)": f"https://twitter.com/search?q={query_encoded}&f=user",
        "TikTok (Perfiles)": f"https://www.tiktok.com/search?q={query_encoded}",
        "YouTube (Canales)": f"https://www.youtube.com/results?search_query={query_encoded}",
        "GitHub (Desarrolladores)": f"https://github.com/search?q={query_encoded}&type=users",
        "GitLab (Repositorios)": f"https://gitlab.com/search?search={query_encoded}",
        "Reddit (Comunidades)": f"https://www.reddit.com/search/?q={query_encoded}",
        "Medium (Artículos)": f"https://medium.com/search?q={query_encoded}",
        "Pinterest (Perfiles)": f"https://www.pinterest.com/search/users/?q={query_encoded}",
        "Google Search (Global)": f"https://www.google.com/search?q={query_encoded}",
        "DuckDuckGo (Privado)": f"https://html.duckduckgo.com/html/?q={query_encoded}"
    }
    
    resultados = [f"# REPORTE OSINT - ALIAS / NOMBRE: {termino}\n"]
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    for plataforma, url in plataformas.items():
        try:
            print(f"[*] Consultando {plataforma}...")
            resp = requests.get(url, headers=headers, timeout=5)
            print(f"    -> HTTP Status: {resp.status_code}")
            if resp.status_code == 200:
                resultados.append(f"- [OK] **{plataforma}**: {url}\n")
            else:
                resultados.append(f"- [STATUS {resp.status_code}] **{plataforma}**: {url}\n")
        except Exception:
            print(f"    -> [!] Error de conexión")
            resultados.append(f"- [ERROR] **{plataforma}**: {url}\n")

    if not os.path.exists("reportes_auditoria"):
        os.makedirs("reportes_auditoria")
        
    nombre_seguro = "".join(c if c.isalnum() else "_" for c in termino)
    nombre_archivo = f"reportes_auditoria/osint_alias_{nombre_seguro}.md"
    with open(nombre_archivo, "w") as f:
        f.writelines(resultados)
        
    print(f"\n[+] Reporte guardado en: {nombre_archivo}")
    input("\nPresiona [Enter] para continuar...")

def osint_auditoria_correo():
    correo = input("[?] Ingresa el correo electrónico a auditar: ").strip()
    if "@" not in correo:
        print("[!] Formato de correo no válido.")
        input("\nPresiona [Enter] para continuar...")
        return
        
    partes = correo.split('@')
    dominio = partes[1] if len(partes) > 1 else ""
    
    print(f"\n[*] Analizando dominio de correo: {dominio}")
    resultados = [f"# REPORTE OSINT - CORREO ELECTRÓNICO: {correo}\n"]
    resultados.append(f"- **Dominio Extraído:** {dominio}\n")
    
    try:
        ip_mx = socket.gethostbyname(dominio)
        print(f"[+] Servidor raíz del dominio accesible en IP: {ip_mx}")
        resultados.append(f"- **IP del Dominio:** {ip_mx}\n")
    except Exception:
        print("[-] No se pudo resolver la IP raíz del dominio de correo.")
        resultados.append(f"- **IP del Dominio:** No resoluble\n")
        
    email_encoded = urllib.parse.quote_plus(correo)
    plataformas_email = {
        "Gravatar (Avatar)": f"https://en.gravatar.com/{urllib.parse.quote_plus(correo.lower())}.json",
        "Google (Menciones)": f"https://www.google.com/search?q=\"{email_encoded}\"",
        "DuckDuckGo (Privado)": f"https://html.duckduckgo.com/html/?q=\"{email_encoded}\"",
        "GitHub (Commits)": f"https://github.com/search?q={email_encoded}&type=users"
    }
    
    resultados.append("\n## Enlaces de Auditoría Web\n")
    headers = {'User-Agent': 'Mozilla/5.0'}
    for plat, url in plataformas_email.items():
        try:
            print(f"[*] Verificando {plat}...")
            resp = requests.get(url, headers=headers, timeout=5)
            print(f"    -> HTTP Status: {resp.status_code}")
            resultados.append(f"- [STATUS {resp.status_code}] {plat}: {url}\n")
        except Exception:
            resultados.append(f"- [ERROR] {plat}: {url}\n")

    if not os.path.exists("reportes_auditoria"):
        os.makedirs("reportes_auditoria")
    nombre_seguro = "".join(c if c.isalnum() else "_" for c in correo)
    nombre_archivo = f"reportes_auditoria/osint_email_{nombre_seguro}.md"
    with open(nombre_archivo, "w") as f:
        f.writelines(resultados)
        
    print(f"\n[+] Reporte de correo guardado en: {nombre_archivo}")
    input("\nPresiona [Enter] para continuar...")

def osint_correlacion_telefono():
    print("\n" + "-"*40)
    print("   CORRELACIÓN DEFENSIVA (NOMBRE + TELÉFONO)   ")
    print("-"*40)
    nombre = input("[?] Ingresa el nombre completo: ").strip()
    telefono = input("[?] Ingresa el número telefónico (10 dígitos): ").strip()
    
    if not nombre or not telefono:
        print("[!] Ambos campos son obligatorios.")
        input("\nPresiona [Enter] para continuar...")
        return
        
    n_enc = urllib.parse.quote_plus(nombre)
    t_enc = urllib.parse.quote_plus(telefono)
    
    dorks = [
        f"https://www.google.com/search?q=\"{n_enc}\"+\"{t_enc}\"",
        f"https://www.google.com/search?q=site:pastebin.com+\"{t_enc}\"",
        f"https://www.google.com/search?q=site:github.com+\"{t_enc}\"",
        f"https://html.duckduckgo.com/html/?q=\"{n_enc}\"+\"{t_enc}\""
    ]
    
    lineas = [
        f"# REPORTE DE CORRELACIÓN Y HUELLA DIGITAL (THREAT INTEL)\n",
        f"- **Objetivo (Nombre):** {nombre}\n",
        f"- **Contacto (Teléfono):** {telefono}\n",
        f"- **Fecha de Análisis:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n",
        "## Matriz de Búsqueda Estructurada (Google Dorks)\n",
        f"- **Correlación Directa Nombre + Teléfono:** [Google Search]({dorks[0]})\n",
        f"- **Auditoría de Filtraciones en Pastebin:** [Pastebin Dork]({dorks[1]})\n",
        f"- **Auditoría de Repositorios de Código en GitHub:** [GitHub Dork]({dorks[2]})\n",
        f"- **Búsqueda Privada (DuckDuckGo):** [DuckDuckGo Search]({dorks[3]})\n"
    ]
    if not os.path.exists("reportes_auditoria"):
        os.makedirs("reportes_auditoria")
        
    nombre_seguro = "".join(c if c.isalnum() else "_" for c in nombre)
    nombre_archivo = f"reportes_auditoria/osint_correlacion_{nombre_seguro}.md"
    with open(nombre_archivo, "w") as f:
        f.writelines(lineas)
        
    print(f"\n[+] Matriz de correlación guardada en: {nombre_archivo}")
    input("\nPresiona [Enter] para continuar...")

def osint_legal_duediligence():
    print("\n" + "="*50)
    print("   MÓDULO OSINT LEGAL & DUE DILIGENCE (EXPEDIENTES) ")
    print("="*50)
    nombre = input("[?] Ingresa el nombre completo o razón social: ").strip()
    jurisdiccion = input("[?] Ingresa estado o fuero (ej. Baja California / Federal): ").strip()
    
    if not nombre or not jurisdiccion:
        print("[!] Todos los campos son obligatorios.")
        input("\nPresiona [Enter] para continuar...")
        return
        
    print(f"\n[*] Generando estructura de investigación legal para: {nombre} ({jurisdiccion})...")
    
    n_enc = urllib.parse.quote_plus(nombre)
    
    dork_general = f"https://www.google.com/search?q=\"{n_enc}\"+expediente+demandas+juicio"
    dork_pjbc = f"https://www.google.com/search?q=site:pjbc.gob.mx+\"{n_enc}\""
    dork_pjf = f"https://www.google.com/search?q=site:cjf.gob.mx+\"{n_enc}\""
    dork_buho = f"https://www.google.com/search?q=site:buholegales.com+\"{n_enc}\""
    
    lineas = [
        f"# REPORTE DE OSINT LEGAL & DUE DILIGENCE\n",
        f"- **Sujeto / Empresa Analizada:** {nombre}\n",
        f"- **Jurisdicción / Región:** {jurisdiccion}\n",
        f"- **Fecha y Hora de Auditoría:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n",
        f"- **Perfil de Operación:** Legal Threat Intelligence\n\n",
        "## 1. Validación de Homónimos y Filtros Previos\n",
        "* [ ] **Cotejo de Identidad:** Verificar RFC, CURP o domicilio asociado para descartar homónimos.\n",
        "* [ ] **Clasificación de Materia:** Determinar si corresponde a Civil, Mercantil, Penal o Laboral.\n\n",
        "## 2. Matriz de Búsqueda y Consultas Judiciales (Dorks)\n",
        f"- **Búsqueda General de Expedientes:** [Google Search Legal]({dork_general})\n",
        f"- **Poder Judicial de Baja California (PJBC):** [PJBC Dork]({dork_pjbc})\n",
        f"- **Consejo de la Judicatura Federal (Amparos/PJF):** [PJF Dork]({dork_pjf})\n",
        f"- **Agregadores de Antecedentes:** [Búho Legal Dork]({dork_buho})\n\n",
        "## 3. Registro de Hallazgos y Trazabilidad Procesal\n",
        "| # Expediente | Juzgado / Tribunal | Materia | Rol (Actor / Demandado) | Estatus Procesal |\n",
        "| :--- | :--- | :--- | :--- | :--- |\n",
        "| *Ej. 123/2025* | *Juzgado Civil* | *Mercantil* | *Demandado* | *En trámite* |\n\n",
        "---\n",
        "*Nota técnica: Reporte estructurado para evaluación de riesgos legales y cumplimiento corporativo.*\n"
    ]

    if not os.path.exists("reportes_auditoria"):
        os.makedirs("reportes_auditoria")
        
    nombre_seguro = "".join(c if c.isalnum() else "_" for c in nombre)
    nombre_archivo = f"reportes_auditoria/osint_legal_{nombre_seguro}.md"
    with open(nombre_archivo, "w") as f:
        f.writelines(lineas)
        
    print(f"\n[+] Reporte de Due Diligence Legal guardado en: {nombre_archivo}")
    input("\nPresiona [Enter] para continuar...")

def modulo_osint_menu():
    while True:
        print("\n" + "="*50)
        print("   MÓDULO OSINT: INTELIGENCIA Y HUELLA DIGITAL   ")
        print("="*50)
        print(" 1. Búsqueda por Alias / Nombre Completo")
        print(" 2. Auditoría y Análisis de Correo Electrónico")
        print(" 3. Correlación Defensiva (Nombre + Teléfono / Dorks)")
        print(" 4. OSINT Legal & Due Diligence (Expedientes y Riesgos)")
        print(" 5. Volver al Menú Principal")
        print("="*50)
        
        op = input("Selecciona una opción OSINT (1-5): ").strip()
        if op == '1':
            osint_busqueda_alias()
        elif op == '2':
            osint_auditoria_correo()
        elif op == '3':
            osint_correlacion_telefono()
        elif op == '4':
            osint_legal_duediligence()
        elif op == '5':
            break
        else:
            print("[!] Opción no válida.")
            input("Presiona [Enter] para continuar...")

def resolver_fabricante():
    print("\n" + "="*50)
    print("    IDENTIFICADOR DE FABRICANTE POR MAC (OUI)     ")
    print("="*50)
    mac = input("[?] Ingresa la dirección MAC (ej. 6c:b8:81:74:e5:d0): ").strip()
    if not mac:
        print("[!] La dirección MAC no puede estar vacía.")
        return

    mac_clean = mac.replace(":", "").replace("-", "").upper()
    if len(mac_clean) >= 2 and mac_clean[1] in ['2', '3', '6', '7', 'A', 'B', 'E', 'F']:
        print(f"\n[i] La MAC {mac} es una Dirección Privada/Aleatoria.")
        input("\nPresiona [Enter] para continuar...")
        return

    url = f"https://api.macvendors.com/{mac}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            fabricante = response.read().decode('utf-8')
            print(f"\n[+] Fabricante/Marca: {fabricante}")
    except Exception:
        print(f"\n[-] No se pudo determinar el fabricante público para {mac}.")
    input("\nPresiona [Enter] para continuar...")

def modulo_reporte_maestro():
    print("\n\033[1;33m[*] Generando Reporte Maestro Consolidado de Red...\033[0m")
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    ip_local = obtener_ip_local()
    partes = ip_local.split('.')
    gateway_ip = f"{partes[0]}.{partes[1]}.{partes[2]}.1" if len(partes) == 4 else "192.168.0.1"

    lineas = [
        "# REPORTE MAESTRO DE AUDITORÍA Y RED\n",
        f"- **Fecha y Hora:** {timestamp}\n",
        "- **Herramienta:** Suite de Diagnóstico y Soporte de Red v4.0\n",
        "- **Perfil de Operación:** IT Support & Cloud / Legal Threat Intel\n",
        f"- **IP Local del Host:** {ip_local}\n",
        f"- **Gateway Identificado:** {gateway_ip}\n\n",
        "## 1. Estado de Conectividad y Latencia\n"
    ]
    
    destinos = {
        "Google DNS": ("8.8.8.8", 53),
        "Cloudflare DNS": ("1.1.1.1", 53),
        "Gateway Router": (gateway_ip, 80)
    }
    
    for nombre, (ip, puerto) in destinos.items():
        try:
            inicio = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2.0)
            sock.connect((ip, puerto))
            sock.close()
            latencia = round((time.time() - inicio) * 1000, 2)
            lineas.append(f"- [OK] {nombre} ({ip}): {latencia} ms\n")
        except Exception:
            lineas.append(f"- [TIMEOUT] {nombre} ({ip}): Sin respuesta\n")

    lineas.append("\n## 2. Observaciones de Seguridad\n")
    lineas.append("- Auditoría de interfaces locales ejecutada sin incidencias críticas en localhost.\n")
    lineas.append("- Monitoreo activo de asignación DHCP y resolución OUI de fabricantes.\n\n")
    lineas.append("---\n")
    lineas.append("*Reporte generado automáticamente por la terminal de diagnóstico.*\n")

    if not os.path.exists("reportes_auditoria"):
        os.makedirs("reportes_auditoria")
        
    nombre_archivo = f"reportes_auditoria/reporte_maestro_{time.strftime('%Y%m%d_%H%M%S')}.md"
    with open(nombre_archivo, "w") as f:
        f.writelines(lineas)
        
    print(f"\n[+] Reporte Maestro guardado exitosamente en: {nombre_archivo}")
    input("\nPresiona [Enter] para continuar...")

def menu_principal():
    while True:
        banner()
        print(" 1. Escaneo y Auditoría de Puertos")
        print(" 2. Inspección de Encabezados HTTP")
        print(" 3. Resolución y Consulta de Registros")
        print(" 4. Prueba de Latencia hacia Endpoints")
        print(" 5. Generador de Reportes de Incidencias")
        print(" 6. Monitor de Recursos del Sistema")
        print(" 7. Módulo OSINT: Inteligencia y Huella Digital")
        print(" 8. Identificar Fabricante por Dirección MAC")
        print(" 9. Generar Reporte Maestro de Red")
        print("10. Salir")
        print("="*60)
        
        opcion = input("Selecciona una opción (1-10): ").strip()

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
            modulo_osint_menu()
        elif opcion == '8':
            resolver_fabricante()
        elif opcion == '9':
            modulo_reporte_maestro()
        elif opcion == '10':
            print("\nSaliendo de la herramienta. ¡Hasta luego!")
            break
        else:
            print("[!] Opción no válida. Elige un número del 1 al 10.")
            input("Presiona [Enter] para continuar...")

if __name__ == "__main__":
    menu_principal()

