import streamlit as st
import os
import time
import datetime
import pandas as pd

# --- SYSTEM-SETUP ---
st.set_page_config(page_title="SilasGuardian", page_icon="🛡️", layout="wide")
VAULT_PATH = "sector_3_vault"
if not os.path.exists(VAULT_PATH): os.makedirs(VAULT_PATH)

class SilasGuardian:
    def __init__(self):
        if 'auth_level' not in st.session_state: st.session_state.auth_level = "A0"
        if 'page' not in st.session_state: st.session_state.page = "dashboard"
        if 'login_time' not in st.session_state: st.session_state.login_time = None
        if 'scan_complete' not in st.session_state: st.session_state.scan_complete = False
        if 'chat_log' not in st.session_state: st.session_state.chat_log = []

    def render(self):
        # Dark-Mode Styling
        st.markdown("<style>.stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New'; }</style>", unsafe_allow_html=True)

        # --- LOGIN ---
        if st.session_state.auth_level == "A0":
            st.title("🛡️ SilasGuardian Login")
            ident = st.text_input("Ident", type="password")
            pwd = st.text_input("Sektor-Passwort", type="password")
            if st.button("Initialisieren"):
                if ident.lower() == "silas" and pwd.lower() == "data":
                    st.session_state.auth_level = "A1+"
                    st.session_state.login_time = time.time()
                    st.rerun()
            return

        # --- TIMER-LOGIK (Die 10-Sekunden-Begrüßung) ---
        elapsed = time.time() - st.session_state.login_time
        if elapsed < 10:
            st.title("Willkommen Anton")
            st.caption(f"System-Vollzugriff aktiv... (Sicherheits-Banner verschwindet in {10 - int(elapsed)}s)")
            # Autorefresh nach 10 Sekunden erzwingen
            time.sleep(1)
            st.rerun()
        else:
            st.title("🛡️ SilasGuardian | Core-Terminal")

        # --- NAVIGATION ---
        tabs = st.tabs(["📡 Deep-Scanner", "📂 Vault", "💬 Comms-Bridge", "🛡️ Sektor Zero"])

        # 1. SCANNER
        with tabs[0]:
            st.subheader("📡 Deep-Net-Inspector")
            if st.button("Deep Scan starten"):
                st.session_state.scan_complete = False
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.02)
                    progress_bar.progress(i + 1)
                st.session_state.scan_complete = True
            
            if st.session_state.scan_complete:
                st.divider()
                scan_data = [
                    {"IP": "192.168.1.1", "Gerät": "FritzBox 7590", "MAC": "00:E0:4C:53:12:01"},
                    {"IP": "192.168.1.42", "Gerät": "Apple iPhone 15", "MAC": "7C:D1:C3:94:02:88"},
                    {"IP": "192.168.1.102", "Gerät": "Samsung SmartTV", "MAC": "BC:DE:F1:00:22:33"}
                ]
                st.table(pd.DataFrame(scan_data))

        # 2. VAULT
        with tabs[1]:
            st.subheader("📂 Sektor 3: Vault")
            up = st.file_uploader("Datei sichern")
            if up:
                with open(os.path.join(VAULT_PATH, up.name), "wb") as f: f.write(up.getbuffer())
                st.success("Gespeichert.")
            for f in os.listdir(VAULT_PATH):
                st.write(f"🔒 {f}")

        # 3. COMMS-BRIDGE (Chat - WIEDER DA!)
        with tabs[2]:
            st.subheader("💬 Comms-Bridge (Verschlüsselt)")
            msg = st.text_input("Nachricht an Silas...")
            if st.button("Senden"):
                t = datetime.datetime.now().strftime("%H:%M")
                st.session_state.chat_log.append(f"[{t}] Anton: {msg}")
            
            st.divider()
            for chat in reversed(st.session_state.chat_log):
                st.info(chat)

        # 4. SEKTOR ZERO
        with tabs[3]:
            st.subheader("🛡️ Sektor Zero")
            if st.button("🚨 System Shutdown (A0)"):
                st.session_state.auth_level = "A0"
                st.rerun()

if __name__ == "__main__":
    SilasGuardian().render()
