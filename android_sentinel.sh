#!/usr/bin/env bash
# ====================================================
# Android Sentinel & System Anomaly Detector
# Compatible con Termux (No-Root)
# ====================================================

ROJO="\e[31m"
VERDE="\e[32m"
AMARILLO="\e[33m"
AZUL="\e[34m"
FIN="\e[0m"

pausa() {
    echo -e "\n${AMARILLO}Presiona [Enter] para continuar...${FIN}"
    read
}

limpiar() {
    clear
}

while true; do
    limpiar
    echo -e "${AZUL}====================================================${FIN}"
    echo -e "${AZUL}        ANDROID SENTINEL - SEGURIDAD Y SISTEMA       ${FIN}"
    echo -e "${AZUL}====================================================${FIN}"
    echo -e "1. Auditoría de Aplicaciones de Usuario (APK / Rutas)"
    echo -e "2. Análisis de Procesos Activos (Anomalías de CPU/Memoria)"
    echo -e "3. Escaneo de Conexiones y Sockets de Red Activos"
    echo -e "4. Resumen Estadístico de Paquetes Instalados"
    echo -e "5. Salir"
    echo -e "${AZUL}====================================================${FIN}"
    read -p "Selecciona una opción [1-5]: " opcion

    case $opcion in
        1)
            limpiar
            echo -e "${VERDE}[*] Analizando aplicaciones de terceros instaladas...${FIN}"
            echo -e "${AMARILLO}Mostrando paquetes y rutas de origen:${FIN}\n"
            pm list packages -3 -f
            pausa
            ;;
        2)
            limpiar
            echo -e "${VERDE}[*] Analizando procesos en ejecución en el sistema...${FIN}"
            echo -e "${AMARILLO}Buscando procesos anómalos o desconocidos:${FIN}\n"
            ps -ef
            pausa
            ;;
     3)
         limpiar
         echo -e "${VERDE}[*] Verificando conexiones de red activas (Termux)...${FIN}"
         netstat -an 2>/dev/null || ss -tu 2>/dev/null
         echo -e "\n${AMARILLO}Rutas de red activas en el dispositivo:${FIN}"
         ip route
         pausa
         ;;


       4)
            limpiar
            echo -e "${VERDE}[*] Estadísticas generales de paquetes del sistema...${FIN}"
            TOTAL_SYS=$(pm list packages -s | wc -l)
            TOTAL_USR=$(pm list packages -3 | wc -l)
            TOTAL_ALL=$(pm list packages | wc -l)
            echo -e "--------------------------------------------------"
            echo -e " Paquetes del sistema (OEM/Google): ${AMARILLO}$TOTAL_SYS${FIN}"
            echo -e " Aplicaciones de usuario (Terceros): ${VERDE}$TOTAL_USR${FIN}"
            echo -e " Total de paquetes registrados:     ${AZUL}$TOTAL_ALL${FIN}"
            echo -e "--------------------------------------------------"
            pausa
            ;;
        5)
            echo -e "${AZUL}Saliendo de Android Sentinel. ¡Hasta luego!${FIN}"
            exit 0
            ;;
        *)
            echo -e "${ROJO}Opción inválida. Selecciona un número del 1 al 5.${FIN}"
            sleep 1
            ;;
    esac
done

