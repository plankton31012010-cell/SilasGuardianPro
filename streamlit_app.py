import streamlit as st
import os
import time
import random
import datetime
import pandas as pd

# --- KONFIGURATION ---
st.set_page_config(page_title="SilasGuardian", page_icon="🛡️", layout="wide")
VAULT_PATH = "sector_3_vault"
if not os.path.exists(VAULT_PATH): os.makedirs(VAULT_PATH)

class SilasGuardian:
    def __init__(self):
        if 'auth_level' not in st.session_state: st.session_state.auth_level = "A0"
        if 'page' not in st.session_state: st.session_state.page = "dashboard"
        if 'login_time' not in st.session_state: st.session_state.login_time = time.time()
        if 'scan_complete' not in st.session_state: st.session_state.scan_complete = False

    def render(self):
        # Dark-Mode Styling
        st.markdown("<style>.stApp { background-color: #050505; color: #00ff41; }</style>", unsafe_allow_html=True)

        # --- LOGIN CHECK ---
        if st.session_state.auth_level == "A0":
            st.title("🛡️ SilasGuardian Login")
            ident = st.text_input("Ident", type="password")
            pwd = st.text_input("Sektor-Passwort", type="password")
            if st.button("Initialisieren"):
                if ident.lower() == "silas" and pwd.lower() == "data":
                    st.session_state.auth_level = "A1+"
                    st.session_state.login_time = time.time() # Start der 10 Sek
                    st.rerun()
            return

        # --- DASHBOARD NAVIGATION ---
        # Funktion: Begrüßungs-Timer (Verschwindet nach 10 Sek)
        elapsed = time.time() - st.session_state.login_time
        if elapsed < 10:
            st.title("Willkommen Anton")
            st.caption(f"Systemzugriff gewährt vor {int(elapsed)} Sekunden...")
        else:
            st.title("🛡️ SilasGuardian | Core-Terminal")

        tabs = st.tabs(["📡 Deep-Scanner", "📂 Vault", "🛡️ Sektor Zero"])

        with tabs[0]:
            st.subheader("Deep-Net-Inspector v2.0")
            if st.button("Deep Scan starten"):
                st.session_state.scan_complete = False
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Simulation des Scans
                for i in range(100):
                    time.sleep(0.02) # Geschwindigkeit des Scans
                    progress_bar.progress(i + 1)
                    status_text.text(f"Analysiere Subnetz-Pakete... {i+1}%")
                
                st.session_state.scan_complete = True
                status_text.success("Scan abgeschlossen. Ergebnisse werden dechiffriert.")

            # Funktion: Ergebnisse erst nach Abschluss anzeigen
            if st.session_state.scan_complete:
                st.divider()
                st.write("### Identifizierte Netzwerk-Entitäten:")
                scan_data = [
                    {"IP": "192.168.1.1", "MAC": "00:E0:4C:53:12:01", "Vendor": "AVM/FritzBox", "Status": "GATEWAY"},
                    {"IP": "192.168.1.42", "MAC": "7C:D1:C3:94:02:88", "Vendor": "Apple Inc.", "Status": "STATION"},
                    {"IP": "192.168.1.102", "MAC": "BC:DE:F1:00:22:33", "Vendor": "Samsung IoT", "Status": "STATION"}
                ]
                st.table(pd.DataFrame(scan_data))

        with tabs[1]:
            st.subheader("Sektor 3: Vault")
            up = st.file_uploader("Datei sichern")
            if up:
                with open(os.path.join(VAULT_PATH, up.name), "wb") as f: f.write(up.getbuffer())
                st.success("Datei im Vault abgelegt.")
            
            for f in os.listdir(VAULT_PATH):
                st.write(f"🔒 {f}")

        with tabs[2]:
            st.subheader("Sektor Zero: Override")
            if st.button("🚨 System Shutdown (A0)"):
                st.session_state.auth_level = "A0"
                st.rerun()

if __name__ == "__main__":
    SilasGuardian().render()
