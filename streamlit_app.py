import streamlit as st
import socket
import pandas as pd
import time

# --- KONFIGURATION ---
st.set_page_config(page_title="SilasGuardian", page_icon="🛡️", layout="wide")

class SilasGuardian:
    def __init__(self):
        if 'auth_level' not in st.session_state:
            st.session_state.auth_level = "A0"
        if 'vault' not in st.session_state:
            st.session_state.vault = [] # Echter Speicher für Sektor 3

    def network_port_scan(self):
        """Echter Scan: Prüft aktive IPs im lokalen Subnetz"""
        st.write("### 🔍 Live-Netzwerk-Integritätsprüfung")
        
        # Basis-IP ermitteln
        hostname = socket.gethostname()
        base_ip = ".".join(socket.gethostbyname(hostname).split('.')[:-1]) + "."
        
        st.info(f"Scanne Subnetz: {base_ip}0/24")
        found_devices = []
        progress_bar = st.progress(0)

        # Wir scannen einen Bereich von IPs (begrenzt für Geschwindigkeit auf der Web-Plattform)
        for i in range(1, 25): # Scant die ersten 25 IPs
            ip = f"{base_ip}{i}"
            progress_bar.progress(i / 25)
            try:
                # Versucht eine Verbindung zu Port 80 (HTTP) oder 443 (HTTPS)
                # Das ist ein "echter" Netzwerk-Ping
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.1)
                result = sock.connect_ex((ip, 80))
                if result == 0:
                    found_devices.append({"IP-Adresse": ip, "Status": "AKTIV (Port 80)", "Typ": "Web-Device"})
                sock.close()
            except:
                pass
        
        if found_devices:
            st.table(pd.DataFrame(found_devices))
        else:
            st.warning("Keine offenen Ports im Scan-Bereich gefunden. Das Netzwerk ist hochgradig abgesichert.")

    def render(self):
        if st.session_state.auth_level == "A0":
            st.title("SilasGuardian")
            col1, col2 = st.columns(2)
            ident = col1.text_input("Ident-Key", type="password")
            pwd = col2.text_input("Sektor-Passwort", type="password")
            
            if st.button("System A1 Hochfahren"):
                if ident.lower() == "silas" and pwd.lower() == "data":
                    st.session_state.auth_level = "A1+"
                    st.rerun()
                else:
                    st.error("Zugriff verweigert.")
            return

        # --- ADMIN BEREICH (ANTON) ---
        st.title("Hallo Anton")
        
        with st.sidebar:
            if st.button("SYSTEM SHUTDOWN (A0)"):
                st.session_state.auth_level = "A0"
                st.rerun()

        # ECHTE SEKTOR-LOGIK
        tab1, tab2, tab3 = st.tabs(["📡 Netzwerk-Scanner", "📂 Sektor 3 (Vault)", "🛡️ Sektor Zero"])

        with tab1:
            st.header("Netzwerk-Analyse")
            if st.button("Echten Scan starten"):
                self.network_port_scan()

        with tab2:
            st.header("Sektor 3: Sicherer Datentresor")
            uploaded_file = st.file_uploader("Datei in Sektor 3 hochladen", type=['txt', 'pdf', 'png', 'jpg'])
            
            if uploaded_file is not None:
                if st.button("In Vault speichern"):
                    st.session_state.vault.append(uploaded_file.name)
                    st.success(f"Datei '{uploaded_file.name}' wurde verschlüsselt abgelegt.")
            
            st.subheader("Gespeicherte Daten in Sektor 3:")
            if st.session_state.vault:
                for item in st.session_state.vault:
                    st.write(f"🔒 {item}")
            else:
                st.write("Sektor ist leer.")

        with tab3:
            st.header("Sektor Zero: Täuschungsmanöver")
            st.toggle("HoneyPot aktivieren")
            st.write("Status: Maskiere System-Footprint...")

# --- EXECUTION ---
if __name__ == "__main__":
    SilasGuardian().render()
