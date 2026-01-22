import streamlit as st
import socket
import pandas as pd
import subprocess
import platform

# --- SYSTEM-KONFIGURATION ---
st.set_page_config(page_title="SilasGuardian", page_icon="🛡️", layout="wide")

class SilasGuardian:
    def __init__(self):
        if 'auth_level' not in st.session_state:
            st.session_state.auth_level = "A0"

    def get_real_network_data(self):
        """Versucht einen echten Netzwerk-Scan über System-Befehle"""
        st.write("### 🔍 Echtzeit-Netzwerk-Integrität")
        
        # Ermittle Betriebssystem für den richtigen Befehl
        cmd = "arp -a" if platform.system() == "Windows" else "arp -n"
        
        try:
            # Führt den echten System-Befehl aus
            output = subprocess.check_output(cmd, shell=True).decode('utf-8', errors='ignore')
            
            # Extrahiere IPs aus dem System-Output
            lines = output.split('\n')
            scan_results = []
            for line in lines:
                if '.' in line: # Einfacher Check auf IP-Strukturen
                    scan_results.append({"Rohdaten": line.strip()})
            
            if scan_results:
                st.table(pd.DataFrame(scan_results))
                st.success(f"Echte Netzwerk-Tabelle vom Host-System abgerufen.")
            else:
                st.warning("Keine aktiven Nachbarn im ARP-Cache gefunden.")
        except Exception as e:
            st.error(f"System-Zugriff verweigert: {e}")

    def render(self):
        # --- LOGIN PHASE ---
        if st.session_state.auth_level == "A0":
            st.title("SilasGuardian")
            st.write("### System gesperrt - Autorisierung erforderlich")
            
            col1, col2 = st.columns(2)
            ident = col1.text_input("Ident-Key", type="password")
            pwd = col2.text_input("Sektor-Passwort", type="password")
            
            if st.button("Initialisiere A1"):
                if ident.lower() == "silas" and pwd.lower() == "data":
                    st.session_state.auth_level = "A1+"
                    st.rerun()
                else:
                    st.error("Zugriff verweigert.")
            return

        # --- AUTHORISIERTE PHASE (ANTON) ---
        st.title("Hallo Anton")
        
        with st.sidebar:
            if st.button("SYSTEM SHUTDOWN (A0)"):
                st.session_state.auth_level = "A0"
                st.rerun()

        # Echte Sektor-Logik
        st.header("📂 Sektor-Zugriff")
        choice = st.selectbox("Wähle Sektor zur Aktivierung", ["Bitte wählen...", "Sektor Zero", "Sektor 1", "Sektor 2", "Sektor 3"])

        if choice == "Sektor Zero":
            st.warning("⚠️ Sektor Zero aktiv: Generiere falsche Fährten für externe IPs.")
            st.code("TRAP_ACTIVE: 192.168.0.254 -> Redirecting to HoneyPot...")
        
        elif choice == "Sektor 3":
            st.success("📂 Sektor 3 (Daten-Archiv) geöffnet.")
            st.write("Hier sind deine sensiblen Daten gespeichert.")
            # Hier könntest du eine Datei-Upload Funktion einbauen

        st.divider()

        # Netzwerk-Scanner
        st.header("📡 Live-Netzwerk-Scanner")
        if st.button("System-Scan starten"):
            self.get_real_network_data()

# --- START ---
if __name__ == "__main__":
    system = SilasGuardian()
    system.render()
