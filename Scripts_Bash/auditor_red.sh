#!/bin/bash

# Colores para la interfaz
VERDE="\033[1;32m"
AZUL="\033[1;34m"
ROJO="\033[1;31m"
CYAN="\033[1;36m"
FIN="\033[0m"

limpiar() {
    clear
}

banner() {
    echo -e "${CYAN}====================================================${FIN}"
    echo -e "${VERDE}    SUITE INTEGRAL: SECURITY & IT SUPPORT (TERMUX) ${FIN}"
    echo -e "${CYAN}====================================================${FIN}"
}

pausa() {
    echo -e "\n${CYAN}Presiona [Enter] para continuar...${FIN}"
    read
}

while true; do
    limpiar
    banner
    echo "--- RED Y PERÍMETRO ---"
    echo "1. Verificar Estado y Latencia (Ping)"
    echo "2. Consultar Tabla ARP Local (ip neigh)"
    echo "3. Escaneo de Puertos TCP Básicos (Nmap -sT)"
    echo "4. Inspección de Cabeceras HTTP (Curl)"
    echo "5. Conexión y Banner Grabbing (Netcat)"
    echo ""
    echo "--- PRIVACIDAD Y TÚNELES (VPN / DNS) ---"
    echo "6. Consultar IP Pública y Geolocalización"
    echo "7. Verificación de Interfaces de Red y VPN (tun0)"
    echo "8. Prueba de Fuga de DNS (Dig + OpenDNS)"
    echo ""
    echo "--- MONITOR, AUDITORÍA Y ALERTAS ---"
    echo "9. Auditoría de Sockets Locales (ss -tuln)"
    echo "10. Monitoreo de Procesos Activos (ps)"
    echo "11. Generar y Guardar Reporte de Auditoría (Log)"
    echo "12. Modo Alertas en Tiempo Real (Filtro Anti-Ruido Avanzado)"
    echo ""
    echo "--- IT & CUSTOMER SUPPORT (APIS / TICKETS) ---"
    echo "13. Probar API / Endpoint / Webhook (Httpie / Curl)"
    echo "14. Registrar Nota Rápida de Incidencia (Bitácora de Soporte)"
    echo "15. Iniciar Sesión Multitarea (Tmux)"
    echo "16. Actualizar Herramientas del Sistema (Pkg Upgrade)"
    echo "17. Salir"
    echo -e "${CYAN}====================================================${FIN}"
    read -p "Elige una opción [1-17]: " opcion

    case $opcion in
        1)
            limpiar
            echo -e "${AZUL}[*] Prueba de Latencia ICMP${FIN}"
            read -p "Ingresa la IP objetivo (ej. 192.168.0.5): " ip_obj
            ping -c 4 "$ip_obj"
            pausa
            ;;
        2)
            limpiar
            echo -e "${AZUL}[*] Consultando dispositivos en la capa de enlace (ARP)${FIN}"
            ip neigh
            pausa
            ;;
        3)
            limpiar
            echo -e "${AZUL}[*] Escaneo de Puertos TCP con Nmap${FIN}"
            read -p "Ingresa la IP objetivo: " ip_obj
            nmap -sT "$ip_obj"
            pausa
            ;;
        4)
            limpiar
            echo -e "${AZUL}[*] Inspección de Cabeceras HTTP con Curl${FIN}"
            read -p "Ingresa la URL o IP (ej. http://192.168.0.1): " url_obj
            curl -I "$url_obj"
            pausa
            ;;
        5)
            limpiar
            echo -e "${AZUL}[*] Conexión y Banner Grabbing con Netcat${FIN}"
            read -p "Ingresa la IP objetivo: " ip_obj
            read -p "Ingresa el puerto (ej. 3000, 7000, 80): " puerto_obj
            nc -v "$ip_obj" "$puerto_obj"
            pausa
            ;;
        6)
            limpiar
            echo -e "${AZUL}[*] Consultando IP Pública y Proveedor...${FIN}"
            curl -s https://ifconfig.me
            echo ""
            curl -s https://ipinfo.io/json
            pausa
            ;;
        7)
            limpiar
            echo -e "${AZUL}[*] Verificando interfaces de red y túneles VPN (tun0)...${FIN}"
            ip a | grep -E "state UP|inet |tun0"
            pausa
            ;;
        8)
            limpiar
            echo -e "${AZUL}[*] Ejecutando Prueba de Fuga de DNS...${FIN}"
            echo -e "${CYAN}Consultando resolución de nombres contra OpenDNS...${FIN}"
            dig +short myip.opendns.com @resolver1.opendns.com
            echo -e "\n${VERDE}Si la IP devuelta coincide con la de tu VPN, tus DNS están blindados.${FIN}"
            pausa
            ;;
        9)
            limpiar
            echo -e "${AZUL}[*] Auditoría de Sockets Locales del Dispositivo${FIN}"
            ss -tuln 2>/dev/null || netstat -tuln
            pausa
            ;;
        10)
            limpiar
            echo -e "${AZUL}[*] Listado de Procesos Activos en Termux${FIN}"
            ps aux
            pausa
            ;;
        11)
            limpiar
            echo -e "${AZUL}[*] Generando y guardando reporte de auditoría...${FIN}"
            LOG_FILE="$HOME/audit_history.log"
            echo "==============================================" >> "$LOG_FILE"
            echo " REPORTE DE AUDITORIA - $(date)" >> "$LOG_FILE"
            echo "==============================================" >> "$LOG_FILE"
            echo "[*] Interfaces de red y VPN activas:" >> "$LOG_FILE"
            ip a | grep -E "state UP|inet |tun0" >> "$LOG_FILE"
            echo "[*] IP Pública actual:" >> "$LOG_FILE"
            curl -s https://ifconfig.me >> "$LOG_FILE"
            echo -e "\n[*] Sockets locales en escucha:" >> "$LOG_FILE"
            ss -tuln 2>/dev/null >> "$LOG_FILE" || netstat -tuln >> "$LOG_FILE"
            echo "----------------------------------------------\n" >> "$LOG_FILE"
            echo -e "${VERDE}[+] Reporte guardado exitosamente en:${FIN} $LOG_FILE"
            pausa
            ;;
        12)
            limpiar
            echo -e "${VERDE}[*] Activando Alertas en Tiempo Real (Modo Silencioso Avanzado)${FIN}"
            echo -e "${CYAN}Ignorando router (IPv4 e IPv6). Vigilando intrusos. Presiona [Ctrl + C] para salir.${FIN}\n"
            
            TEMP_ARP=$(mktemp)
            TEMP_SOCK=$(mktemp)
            # Filtro dual para ignorar tanto la IP del router en v4 como en v6
            ip neigh | grep -vE "192.168.0.1|fe80::10:18ff:fe73:d564" > "$TEMP_ARP"
            ss -tuln 2>/dev/null > "$TEMP_SOCK" || netstat -tuln > "$TEMP_SOCK"
            
            while true; do
                CURRENT_ARP=$(mktemp)
                CURRENT_SOCK=$(mktemp)
                ip neigh | grep -vE "192.168.0.1|fe80::10:18ff:fe73:d564" > "$CURRENT_ARP"
                ss -tuln 2>/dev/null > "$CURRENT_SOCK" || netstat -tuln > "$CURRENT_SOCK"
                
                if ! cmp -s "$TEMP_ARP" "$CURRENT_ARP"; then
                    echo -e "\n${ROJO}[!] ¡ALERTA CRÍTICA! Cambio detectado en los dispositivos de la red:${FIN}"
                    diff "$TEMP_ARP" "$CURRENT_ARP"
                    cp "$CURRENT_ARP" "$TEMP_ARP"
                fi
                
                if ! cmp -s "$TEMP_SOCK" "$CURRENT_SOCK"; then
                    echo -e "\n${ROJO}[!] ¡ALERTA DE DISPOSITIVO! Nuevo puerto/socket abierto:${FIN}"
                    diff "$TEMP_SOCK" "$CURRENT_SOCK"
                    cp "$CURRENT_SOCK" "$TEMP_SOCK"
                fi
                
                sleep 6
                rm "$CURRENT_ARP" "$CURRENT_SOCK"
            done
            rm "$TEMP_ARP" "$TEMP_SOCK"
            pausa
            ;;
        13)
            limpiar
            echo -e "${AZUL}[*] Pruebas de API y Webhooks (Httpie / Curl)${FIN}"
            read -p "Ingresa la URL del Endpoint o Webhook: " api_url
            echo -e "${CYAN}1. Método GET | 2. Método POST${FIN}"
            read -p "Elige el método [1-2]: " metodo
            if [ "$metodo" == "1" ]; then
                http GET "$api_url" 2>/dev/null || curl -i "$api_url"
            else
                read -p "Ingresa los datos JSON (ej. {'key':'value'}): " json_data
                http POST "$api_url" json:="$json_data" 2>/dev/null || curl -X POST -H "Content-Type: application/json" -d "$json_data" "$api_url"
            fi
            pausa
            ;;
        14)
            limpiar
            echo -e "${AZUL}[*] Bitácora de Soporte Técnico (Incidencias)${FIN}"
            read -p "Escribe los detalles del caso o ticket de soporte: " nota_soporte
            SUPPORT_LOG="$HOME/support_tickets.log"
            echo "[$(date)] TICKET: $nota_soporte" >> "$SUPPORT_LOG"
            echo -e "${VERDE}[+] Nota guardada en tu bitácora de soporte.${FIN}"
            pausa
            ;;
        15)
            limpiar
            echo -e "${AZUL}[*] Iniciando multiplexor Tmux para soporte multitarea...${FIN}"
            echo -e "${CYAN}Nota: Si es tu primera vez, usa [Ctrl+B] y luego [%] para dividir paneles.${FIN}"
            sleep 2
            tmux
            pausa
            ;;
        16)
            limpiar
            echo -e "${AZUL}[*] Actualizando paquetes y dependencias...${FIN}"
            pkg update && pkg upgrade -y
            pausa
            ;;
        17)
            echo -e "${VERDE}Saliendo de la herramienta. ¡Mantente seguro y buen soporte!${FIN}"
            exit 0
            ;;
        *)
            echo -e "${ROJO}[!] Opción no válida. Inténtalo de nuevo.${FIN}"
            pausa
            ;;
    esac
done
