import streamlit as st
import time
import random

# --- SYSTEM-KONFIGURATION ---
st.set_page_config(page_title="SilasGuardian", page_icon="🛡️", layout="wide")

class SilasGuardian:
    def __init__(self):
        # Initialisierung des Systemstatus
        if 'auth_level' not in st.session_state:
            st.session_state.auth_level = "A0"
        if 'sectors' not in st.session_state:
            st.session_state.sectors = {
                0: {"name": "Sektor Zero", "status": "Verschleiert"},
                1: {"name": "Kern-System", "status": "Offline"},
                2: {"name": "Comms-Bridge", "status": "Offline"},
                3: {"name": "Sektor 3", "status": "Gesperrt"}
            }

    def run_network_scan(self):
        """Simuliert einen Netzwerk-Scan nach Unregelmäßigkeiten"""
        st.write("### 🔍 Netzwerk-Integritäts-Scan")
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for percent in range(0, 101, 10):
            status_text.text(f"Scanne Subnetz-Pakete... {percent}%")
            progress_bar.progress(percent)
            time.sleep(0.3)
        
        # Zufällige Generierung von 'Unregelmäßigkeiten' zur Simulation
        anomalies = random.randint(0, 2)
        if anomalies == 0:
            st.success("✅ Keine Unregelmäßigkeiten im Netzwerk gefunden. Integrität 100%.")
        else:
            st.warning(f"⚠️ Warnung: {anomalies} verdächtige Pakete in Sektor Zero abgefangen.")

    def startup_sequence(self):
        # 1. Login-Prüfung (Nur wenn nicht eingeloggt)
        if st.session_state.auth_level == "A0":
            st.title("SilasGuardian")
            st.warning("Zugriff verweigert. System im Standby-Modus (A0).")
            
            # Zentrales Eingabefeld (nicht in der Sidebar für maximale Aufmerksamkeit)
            st.divider()
            col1, col2 = st.columns(2)
            with col1:
                ident = st.text_input("Identitäts-Key", type="password", placeholder="Bestätige Identität...")
            with col2:
                pwd = st.text_input("Sektor-Passwort", type="password", placeholder="Sektor-Zuweisung...")
            
            if st.button("System-Initialisierung (A1)"):
                if ident.lower() == "silas" and pwd.lower() == "data":
                    st.session_state.auth_level = "A1+"
                    st.session_state.sectors[1]["status"] = "ONLINE"
                    st.session_state.sectors[2]["status"] = "ONLINE"
                    st.session_state.sectors[3]["status"] = "AKTIVIERT"
                    st.success("Autorisierung erfolgreich. Starte System...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Ungültige Parameter. Zugriffsprotokoll 403.")
            
            # WICHTIG: Hier endet die Anzeige für Unbefugte. Kein Sektor-Status sichtbar!
            return

        # 2. Interface für autorisierte Nutzer (Anton)
        if st.session_state.auth_level == "A1+":
            st.title("Hallo Anton")
            st.sidebar.header("System-Kontrolle")
            
            if st.sidebar.button("System Shutdown (A0)"):
                st.session_state.auth_level = "A0"
                st.rerun()

            # Anzeige der Sektoren (Erst jetzt sichtbar!)
            st.subheader("System-Integrität & Sektoren-Status")
            cols = st.columns(4)
            for i, col in enumerate(cols):
                with col:
                    st.metric(label=st.session_state.sectors[i]["name"], 
                              value=st.session_state.sectors[i]["status"])
            
            st.divider()

            # Netzwerk-Scanner Tool
            st.header("🛠️ Admin-Tools")
            tab1, tab2 = st.tabs(["Netzwerk-Scanner", "Sektor 3 Archiv"])
            
            with tab1:
                if st.button("Netzwerk jetzt scannen"):
                    self.run_network_scan()
            
            with tab2:
                st.write("Willkommen in Sektor 3. Deine verschlüsselten Daten sind hier sicher.")

# --- START ---
system = SilasGuardian()
system.startup_sequence()
