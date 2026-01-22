import streamlit as st
import time
import random

# --- SYSTEM-KONFIGURATION ---
st.set_page_config(page_title="SilasGuardian", page_icon="🛡️", layout="wide")

class SilasGuardian:
    def __init__(self):
        if 'auth_level' not in st.session_state:
            st.session_state.auth_level = "A0"
        if 'sectors' not in st.session_state:
            st.session_state.sectors = {
                0: {"name": "Sektor Zero", "desc": "Täuschungsmodul & False Trail"},
                1: {"name": "Kern-System", "desc": "Zentrale Logik-Einheit"},
                2: {"name": "Comms-Bridge", "desc": "Verschlüsselte Kommunikation"},
                3: {"name": "Sektor 3", "desc": "Archiv-Daten (Verschlüsselt)"}
            }

    def run_network_scan(self):
        """Erweiterter Scanner mit IP-Adressen und Gerätenamen"""
        st.write("### 🔍 Aktive Netzwerk-Teilnehmer")
        
        with st.spinner("Scanne Netzwerksegmente..."):
            time.sleep(2)
            
            # Simulierte Netzwerk-Daten
            devices = [
                {"device": "Haupt-Server (Host)", "ip": "192.168.1.1", "status": "Sicher"},
                {"device": "Anton's Workstation", "ip": "192.168.1.15", "status": "Sicher"},
                {"device": "Unbekanntes Mobilgerät", "ip": "192.168.1.42", "status": "Verdächtig"},
                {"device": "Smart-IoT Gateway", "ip": "192.168.1.102", "status": "Sicher"}
            ]
            
            # Tabellarische Anzeige der Ergebnisse
            st.table(devices)
            st.success(f"Scan abgeschlossen. {len(devices)} Geräte identifiziert.")

    def startup_sequence(self):
        # --- LOGIN-SPERRE ---
        if st.session_state.auth_level == "A0":
            st.title("SilasGuardian")
            st.error("System gesperrt. Bitte Autorisierung eingeben.")
            
            col1, col2 = st.columns(2)
            with col1:
                ident = st.text_input("Identitäts-Key", type="password")
            with col2:
                pwd = st.text_input("Sektor-Passwort", type="password")
            
            if st.button("System A1 Hochfahren"):
                if ident.lower() == "silas" and pwd.lower() == "data":
                    st.session_state.auth_level = "A1+"
                    st.rerun()
                else:
                    st.error("Zugriff verweigert.")
            return

        # --- ADMIN-BEREICH (ANTON) ---
        st.title("Hallo Anton")
        
        # Sidebar für globale Befehle
        with st.sidebar:
            st.header("Admin-Konsole")
            if st.button("System-Shutdown (A0)"):
                st.session_state.auth_level = "A0"
                st.rerun()

        # Sektor-Zugriff (Extra Eingabefelder/Buttons für jeden Sektor)
        st.header("📂 Sektor-Management")
        tabs = st.tabs([s["name"] for s in st.session_state.sectors.values()])

        for i, tab in enumerate(tabs):
            with tab:
                st.subheader(f"Zugriff auf {st.session_state.sectors[i]['name']}")
                st.write(f"**Beschreibung:** {st.session_state.sectors[i]['desc']}")
                
                # Individuelle Sektor-Funktionen
                if st.button(f"Sektor {i} Integrität prüfen", key=f"btn_{i}"):
                    st.info(f"Sektor {i} läuft stabil auf Port 808{i}.")
                
                if i == 3:
                    st.text_area("Daten-Output Sektor 3", "Verschlüsselte Archiv-Daten: [ALPHA-9-DATA-STREAM]")

        st.divider()

        # Netzwerk-Scanner Bereich
        st.header("📡 Netzwerk-Analyse")
        if st.button("Full Network Scan starten"):
            self.run_network_scan()

# --- INITIALISIERUNG ---
system = SilasGuardian()
system.startup_sequence()
