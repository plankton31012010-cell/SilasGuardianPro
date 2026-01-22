import streamlit as st
import time
import socket
import pandas as pd
from scapy.all import ARP, Ether, srp

# --- SYSTEM-KONFIGURATION ---
st.set_page_config(page_title="SilasGuardian", page_icon="🛡️", layout="wide")

class SilasGuardian:
    def __init__(self):
        # Initialisierung der Zustände
        if 'auth_level' not in st.session_state:
            st.session_state.auth_level = "A0"
        if 'sectors' not in st.session_state:
            st.session_state.sectors = {
                0: {"name": "Sektor Zero", "status": "Deceptive/Aktiv", "desc": "Täuschungsmodul für Angreifer."},
                1: {"name": "Kern-System", "status": "Online", "desc": "Zentrale Steuerungseinheit."},
                2: {"name": "Comms-Bridge", "status": "Online", "desc": "Sicherer Datenkanal."},
                3: {"name": "Sektor 3", "status": "Autorisiert", "desc": "Verschlüsselter Datentresor (ehem. Archiv)."}
            }

    def get_local_ip(self):
        """Ermittelt die IP des ausführenden Systems"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 1))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return '127.0.0.1'

    def run_real_scan(self):
        """Führt einen echten ARP-Scan im lokalen Netzwerk aus"""
        st.write("### 🔍 Real-Time Netzwerk-Scan")
        local_ip = self.get_local_ip()
        ip_range = ".".join(local_ip.split('.')[:-1]) + ".0/24"
        
        st.info(f"Zielbereich: {ip_range} (Basierend auf lokaler IP: {local_ip})")
        
        with st.spinner("Sende ARP-Pakete an Netzwerk-Teilnehmer..."):
            try:
                # Erstellung der Netzwerk-Pakete
                arp = ARP(pdst=ip_range)
                ether = Ether(dst="ff:ff:ff:ff:ff:ff")
                packet = ether/arp
                
                # Senden und Empfangen (Echter Scan)
                result = srp(packet, timeout=3, verbose=False)[0]

                devices = []
                for sent, received in result:
                    # Versuche Hostname zu ermitteln
                    try:
                        name = socket.gethostbyaddr(received.psrc)[0]
                    except:
                        name = "Unbekanntes Gerät"
                    
                    devices.append({
                        "IP-Adresse": received.psrc,
                        "MAC-Adresse": received.hwsrc,
                        "Gerätename": name
                    })

                if devices:
                    st.success(f"Scan erfolgreich: {len(devices)} Geräte aktiv.")
                    st.table(pd.DataFrame(devices))
                else:
                    st.warning("Keine Geräte gefunden. Prüfe deine Admin-Rechte.")
            
            except Exception as e:
                st.error(f"Scan-Fehler: {e}")
                st.info("Hinweis: Echte Netzwerk-Scans erfordern
