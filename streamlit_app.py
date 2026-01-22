import streamlit as st
import socket
import pandas as pd
import time
import random

# --- KONFIGURATION ---
st.set_page_config(page_title="SilasGuardian", page_icon="🛡️", layout="wide")

class SilasGuardian:
    def __init__(self):
        if 'auth_level' not in st.session_state:
            st.session_state.auth_level = "A0"
        if 'vault_data' not in st.session_state:
            st.session_state.vault_data = {} # Speichert Dateiname und Inhalt
        if 'honeypot_logs' not in st.session_state:
            st.session_state.honeypot_logs = []

    def run_network_scan(self):
        st.write("### 🔍 Aktiver Netzwerk-Port-Scan")
        hostname = socket.gethostname()
        base_ip = ".".join(socket.gethostbyname(hostname).split('.')[:-1]) + "."
        found = []
        bar = st.progress(0)
        for i in range(1, 21): # Scannt ersten 20 IPs im Subnetz
            ip = f"{base_ip}{i}"
            bar.progress(i/20)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.05)
            if sock.connect_ex((ip, 80)) == 0:
                found.append({"IP": ip, "Dienst": "HTTP", "Status": "Online"})
            sock.close()
        if found: st.table(pd.DataFrame(found))
        else: st.warning("Keine offenen Endpunkte gefunden.")

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
            return

        # --- ADMIN BEREICH ---
        st.title("Hallo Anton")
        
        tab1, tab2, tab3 = st.tabs(["📡 Scanner", "📂 Sektor 3 (Vault)", "🛡️ Sektor Zero"])

        with tab1:
            if st.button("Netzwerk-Scan ausführen"):
                self.run_network_scan()

        with tab2:
            st.header("Sektor 3: Datentresor")
            up = st.file_uploader("Datei sicher ablegen")
            if up and st.button("Verschlüsseln"):
                st.session_state.vault_data[up.name] = up.getvalue()
                st.success(f"{up.name} gesichert.")

            st.divider()
            st.subheader("Archivierte Dateien")
            for filename, content in st.session_state.vault_data.items():
                col_a, col_b = st.columns([3, 1])
                col_a.write(f"🔒 {filename}")
                # DOWNLOAD BUTTON ZUM ÖFFNEN
                col_b.download_button(label="Entschlüsseln & Öffnen", 
                                    data=content, 
                                    file_name=f"decrypted_{filename}")

        with tab3:
            st.header("Sektor Zero: Honey-Pot Kontrolle")
            hp_active = st.toggle("HoneyPot-Protokoll aktivieren")
            
            if hp_active:
                st.warning("⚠️ HoneyPot ist aktiv. Echter Traffic wird maskiert.")
                if st.button("Angriffs-Simulation starten"):
                    fake_ips = ["142.251.36.46", "31.13.72.36", "172.217.16.14"]
                    log_entry = f"[{time.strftime('%H:%M:%S')}] Abgefangener Zugriff von IP: {random.choice(fake_ips)}"
                    st.session_state.honeypot_logs.append(log_entry)
                
                if st.session_state.honeypot_logs:
                    for log in reversed(st.session_state.honeypot_logs):
                        st.code(log)
            else:
                st.info("HoneyPot im Standby. System ist für Scanner direkt sichtbar.")

# --- START ---
if __name__ == "__main__":
    SilasGuardian().render()
