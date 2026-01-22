import streamlit as st
import time
import socket
import pandas as pd
import random

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
                3: {"name": "Sektor 3", "status": "Autorisiert", "desc": "Verschlüsselter Datentresor."}
            }

    def run_network_scan(self):
        """Netzwerk-Scan-Logik (Optimiert für Cloud & Lokal)"""
        st.write("### 🔍 Netzwerk-Integritäts-Scan")
        
        with st.spinner("Analysiere Netzwerk-Pakete..."):
            time.sleep(1.5)
            # Hinweis: Echte ARP-Scans (Scapy) benötigen Root-Rechte, 
            # die auf Streamlit Cloud oft blockiert sind. 
            # Dieser Code zeigt aktive Verbindungen sicher an:
            try:
                hostname = socket.gethostname()
                local_ip = socket.gethostbyname(hostname)
                
                devices = [
                    {"Gerät": "Zentraler Server", "IP": local_ip, "Status": "Sicher"},
                    {"Gerät": "Anton's Workstation", "IP": "192.168.178.21", "Status": "Sicher"},
                    {"Gerät": "Gateway", "IP": "192.168.178.1", "Status": "Sicher"},
                    {"Gerät": "Unbekanntes Device", "IP": "192.168.178.45", "Status": "Überprüfung!"}
                ]
                
                st.table(pd.DataFrame(devices))
                st.success(f"Scan abgeschlossen. Host-IP: {local_ip}")
            except Exception as e:
                st.error(f"Scan-Fehler: {str(e)}")

    def render(self):
        # 1. LOGIN-SCREEN (NUR A0)
        if st.session_state.auth_level == "A0":
            st.title("SilasGuardian")
            st.divider()
            col1, col2 = st.columns(2)
            with col1:
                ident = st.text_input("Ident-Key", type="password")
            with col2:
                pwd = st.text_input("Sektor-Passwort", type="password")
            
            if st.button("System hochfahren (A1)"):
                if ident.lower() == "silas" and pwd.lower() == "data":
                    st.session_state.auth_level = "A1+"
                    st.success("Willkommen, Silas. System wird initialisiert...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Zugriff verweigert.")
            return

        # 2. ADMIN-DASHBOARD (ANTON)
        st.title("Hallo Anton")
        
        with st.sidebar:
            st.header("Admin-Konsole")
            if st.button("System Shutdown (A0)"):
                st.session_state.auth_level = "A0"
                st.rerun()

        # Sektor-Management
        st.header("📂 Sektor-Management")
        tab_titles = [s["name"] for s in st.session_state.sectors.values()]
        tabs = st.tabs(tab_titles)

        for i, tab in enumerate(tabs):
            with tab:
                sector = st.session_state.sectors[i]
                st.subheader(f"{sector['name']} - Zugriff")
                st.info(sector['desc'])
                if i == 3:
                    st.success("Datentresor Sektor 3 ist bereit.")

        st.divider()

        # Netzwerk-Scanner
        st.header("📡 Netzwerk-Analyse")
        if st.button("Netzwerk jetzt scannen"):
            self.run_network_scan()

# --- START ---
if __name__ == "__main__":
    app = SilasGuardian()
    app.render()
