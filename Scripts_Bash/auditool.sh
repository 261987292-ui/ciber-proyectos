#!/bin/bash

# ======================================================
# MI ASISTENTE DE RED Y SEGURIDAD - TERMINAL NIVEL DIOS
# ======================================================

LINEA_BASE="dispositivos_conocidos.txt"
CARPETA_REPORTES="reportes_auditoria"

mkdir -p "$CARPETA_REPORTES"

mostrar_menu() {
    clear
    echo "======================================================"
    echo "         MI ASISTENTE DE RED - TERMINAL DE ELITE     "
    echo "======================================================"
    echo "1. Ver dispositivos conectados (Tabla ARP)"
    echo "2. Escaneo rápido de red local (Nmap)"
    echo "3. Verificar servicio LG/IP 192.168.0.5"
    echo "4. Hacer Ping al enrutador (192.168.0.1)"
    echo "5. Consultar IP pública"
    echo "6. Guardar línea base de dispositivos conocidos"
    echo "7. Detectar dispositivos nuevos (Alerta de red)"
    echo "8. Monitor de Recursos (Almacenamiento y Procesos)"
    echo "9. Auditor de Puertos Locales (Nmap)"
    echo "10. Escáner Avanzado Python (Multihilo + Banner Grabbing)"
    echo "11. Generar Reporte Completo de Red a Archivo"
    echo "12. Salir"
    echo "======================================================"
}

pausa() {
    echo ""
    read -p "Presiona [Enter] para continuar..."
}

while true; do
    mostrar_menu
    read -p "Elige una opción [1-12]: " opcion
    
    case $opcion in
        1)
            echo -e "\n[*] Consultando tabla ARP local..."
            ip neigh
            pausa
            ;;
        2)
            echo -e "\n[*] Ejecutando escaneo rápido en la red..."
            nmap -F 192.168.0.0/24
            pausa
            ;;
        3)
            echo -e "\n[*] Verificando conectividad con 192.168.0.5..."
            ping -c 3 192.168.0.5
            pausa
            ;;
        4)
            echo -e "\n[*] Haciendo Ping al enrutador principal..."
            ping -c 3 192.168.0.1
            pausa
            ;;
        5)
            echo -e "\n[*] Consultando tu dirección IP pública..."
            curl -s ifconfig.me
            echo ""
            pausa
            ;;
        6)
            echo -e "\n[*] Guardando dispositivos actuales como línea base..."
            ip neigh | grep -E "REACHABLE|STALE|DELAY" | awk '{print $1}' | sort -u > "$LINEA_BASE"
            echo "[+] Guardados en $LINEA_BASE:"
            cat "$LINEA_BASE"
            pausa
            ;;
        7)
            echo -e "\n[*] Analizando la red en busca de dispositivos nuevos..."
            if [ ! -f "$LINEA_BASE" ]; then
                echo "[!] No existe una línea base. Ejecuta la opción 6 primero."
            else
                ACTUALES=$(mktemp)
                ip neigh | grep -E "REACHABLE|STALE|DELAY" | awk '{print $1}' | sort -u > "$ACTUALES"
                NUEVOS=$(comm -13 "$LINEA_BASE" "$ACTUALES")
                
                if [ -z "$NUEVOS" ]; then
                    echo "[+] No se detectaron dispositivos nuevos en la red."
                else
                    echo -e "\e[1;31m[!] ¡ALERTA DE SEGURIDAD! Dispositivos nuevos detectados:\e[0m"
                    echo "$NUEVOS"
                fi
                rm "$ACTUALES"
            fi
            pausa
            ;;
        8)
            echo -e "\n[*] Monitor de Almacenamiento:"
            df -h
            echo -e "\n[*] Uso de Memoria y Procesos principales:"
            top -b -n 1 | head -n 15
            pausa
            ;;
        9)
            echo -e "\n[*] Auditando puertos locales abiertos con Nmap..."
            nmap 127.0.0.1
            pausa
            ;;
        10)
            echo -e "\n[*] Módulo Avanzado Python (Multihilo + Banner Grabbing)"
            read -p "Introduce la IP a escanear [Dejar en blanco para 127.0.0.1]: " ip_objetivo
            if [ -z "$ip_objetivo" ]; then
                ip_objetivo="127.0.0.1"
            fi
            
            if [ -f "port_scanner.py" ]; then
                python port_scanner.py "$ip_objetivo"
            else
                echo "[!] Error: No se encuentra el archivo port_scanner.py"
            fi
            pausa
            ;;
        11)
            FECHA=$(date +"%Y%m%d_%H%M%S")
            ARCHIVO_REPORTE="$CARPETA_REPORTES/reporte_red_$FECHA.txt"
            echo -e "\n[*] Generando reporte completo de red..."
            
            {
                echo "======================================================"
                echo " REPORTE DE AUDITORIA DE RED - TERMINAL"
                echo " Fecha y Hora: $(date)"
                echo "======================================================"
                echo -e "\n[1] TABLA ARP:"
                ip neigh
                echo -e "\n[2] CONFIGURACION DE INTERFAZ:"
                ifconfig || ip a
                echo -e "\n[3] CONECTIVIDAD AL ENRUTADOR (PING):"
                ping -c 2 192.168.0.1
            } > "$ARCHIVO_REPORTE"
            
            echo "[+] Reporte guardado exitosamente en: $ARCHIVO_REPORTE"
            pausa
            ;;
        12)
            echo -e "\n¡Hasta luego!"
            exit 0
            ;;
        *)
            echo -e "\nOpción no válida. Intenta de nuevo."
            sleep 1
            ;;
    esac
done
def mostrar_menu():
    print("==================================================")
    print("        MI ASISTENTE DE RED - TERMINAL DE ÉLITE   ")
    print("==================================================")
    print(" 1. Ver dispositivos conectados (Tabla ARP)")
    print(" 2. Escaneo rápido de red local (Nmap)")
    print(" 3. Verificar servicio LG/IP 192.168.0.5")
    print(" 4. Hacer Ping al enrutador (192.168.0.1)")
    print(" 5. Consultar IP pública")
    print(" 6. Guardar línea base de dispositivos conocidos")
    print(" 7. Detectar dispositivos nuevos (Alerta de red)")
    print(" 8. Monitor de Recursos (Almacenamiento y Procesos)")
    print(" 9. Auditor de Puertos Locales (Nmap)")
    print("10. Escaner Avanzado Python (Multihilo + Banner Grabbing)")
    print("11. Generar Reporte Completo de Red a Archivo")
    print("12. Módulo OSINT: Búsqueda de Alias / Huella Digital")
    print("13. Salir")

