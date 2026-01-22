import streamlit as st
import socket
import time
import pandas as pd
from scapy.all import ARP, Ether, srp

# --- SYSTEM-KONFIGURATION ---
st.set_page_config(page_title="SilasGuardian", page_icon="🛡️", layout="wide")

class SilasGuardian:
    def __init__(self):
        if 'auth_level' not in st.session_state:
            st.session_state.auth_level = "A0"

    def get_local_ip(self):
        """Ermittelt die IP-Adresse deines Computers im Netzwerk"""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 1))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip

    def real_network_scan(self):
        """Führt einen echten ARP-Scan im lokalen Netzwerk aus"""
        local_ip = self.get_local_ip()
        # Erstellt den IP-Bereich (z.B. 192.168.1.0/24)
        ip_range = ".".join(local_ip.split('.')[:-1]) + ".0/24"
        
        st.write(f"### 🔍 Scanne echtes Netzwerk: `{ip_range}`")
        progress = st.progress(0)
        
        try:
            # Erstelle ARP-Anfrage
            arp = ARP(pdst=ip_range)
            ether = Ether(dst="ff:ff:ff:ff:ff:ff")
            packet = ether/arp

            # Sende Paket und empfange Antwort (Timeout 2 Sek)
            result = srp(packet, timeout=2, verbose=False)[0]

            devices = []
            for sent, received in result:
                # Versuche den Namen des Geräts (Hostname) zu finden
                try:
                    hostname = socket.gethostbyaddr(received.psrc)[0]
                except:
                    hostname = "Unbekanntes Gerät"
                
                devices.append({'IP-Adresse': received.psrc, 'MAC-Adresse': received.hwsrc, 'Gerätename': hostname})

            if devices:
                df = pd.DataFrame(devices)
                st.table(df)
                st.success(f"Scan abgeschlossen. {len(devices)} aktive Geräte gefunden.")
            else:
                st.warning("Keine Geräte gefunden. Bist du sicher, dass du Admin-Rechte hast?")
                
        except Exception as e:
            st.error(f"Fehler beim Zugriff auf Netzwerk-Interface: {e}")
            st.info("Hinweis: Echte Netzwerk-Scans benötigen Administrator-Rechte (sudo/admin).")

    def startup_sequence(self):
        if st.session_state.auth_level == "A0":
            st.title("SilasGuardian")
            col1, col2 = st.columns(2)
            ident = col1.text_input("Identitäts-Key", type="password")
            pwd = col2.text_input("Sektor-Passwort", type="password")
            
            if st.button("System A1 Hochfahren"):
                if ident.lower() == "silas" and pwd.lower() == "data":
                    st.session_state.auth_level = "A1+"
                    st.rerun()
            return

        # ADMIN-BEREICH (ANTON)
        st.title("Hallo Anton")
        st.sidebar.button("Shutdown (A0)", on_click=lambda: st.session_state.update({"auth_level": "A0"}))

        st.header("📡 Real-Time Netzwerk-Analyse")
        if st.button("Echten Scan jetzt starten"):
            self.real_network_scan()

# --- START ---
system = SilasGuardian()
system.startup_sequence()
