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
        if 'login_time' not in st.session_state: st.session_state.login_time = None
        if 'scan_status' not in st.session_state: st.session_state.scan_status = "idle"
        if 'chat_log' not in st.session_state: st.session_state.chat_log = []

    def render(self):
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

        # --- DYNAMISCHE BEGRÜSSUNG (Timer Fix) ---
        elapsed = time.time() - st.session_state.login_time
        if elapsed < 10:
            st.title("Willkommen Anton")
            st.caption(f"Sicherheits-Banner aktiv... ({10 - int(elapsed)}s)")
            time.sleep(1)
            st.rerun()
        else:
            st.title("🛡️ SilasGuardian | Core-Terminal")

        # --- MODULE ---
        tabs = st.tabs(["📡 Deep-Scanner", "📂 Sektor 3 (Vault)", "💬 Comms-Bridge", "🛡️ Sektor Zero"])

        # 1. SCANNER MIT FIX
        with tabs[0]:
            st.subheader("📡 Deep-Net-Inspector")
            if st.button("Deep Scan starten"):
                st.session_state.scan_status = "running"
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.02)
                    progress_bar.progress(i + 1)
                st.session_state.scan_status = "complete"
            
            if st.session_state.scan_status == "complete":
                st.success("Scan erfolgreich abgeschlossen.")
                scan_data = [
                    {"IP": "192.168.1.1", "Gerät": "FritzBox 7590", "MAC": "00:E0:4C:53:12:01", "Status": "Online"},
                    {"IP": "192.168.1.42", "Gerät": "Apple iPhone 15", "MAC": "7C:D1:C3:94:02:88", "Status": "Online"},
                    {"IP": "192.168.1.102", "Gerät": "Samsung SmartTV", "MAC": "BC:DE:F1:00:22:33", "Status": "Standby"}
                ]
                st.table(pd.DataFrame(scan_data))

        # 2. VAULT MIT ÖFFNEN-FUNKTION
        with tabs[1]:
            st.subheader("📂 Sektor 3: Datentresor")
            up = st.file_uploader("Datei hochladen")
            if up:
                with open(os.path.join(VAULT_PATH, up.name), "wb") as f: f.write(up.getbuffer())
                st.success(f"{up.name} gesichert.")
            
            st.divider()
            files = os.listdir(VAULT_PATH)
            if files:
                for f_name in files:
                    file_path = os.path.join(VAULT_PATH, f_name)
                    with open(file_path, "rb") as file_bytes:
                        st.download_button(label=f"🔓 {f_name} öffnen", data=file_bytes, file_name=f_name, key=f_name)
            else: st.info("Sektor 3 ist leer.")

        # 3. CHAT
        with tabs[2]:
            st.subheader("💬 Comms-Bridge")
            msg = st.text_input("Nachricht...")
            if st.button("Senden"):
                t = datetime.datetime.now().strftime("%H:%M")
                st.session_state.chat_log.append(f"[{t}] Anton: {msg}")
            
            for chat in reversed(st.session_state.chat_log):
                st.code(chat)

        # 4. SHUTDOWN
        with tabs[3]:
            if st.button("🚨 System Shutdown"):
                st.session_state.auth_level = "A0"
                st.session_state.scan_status = "idle"
                st.rerun()

if __name__ == "__main__":
    SilasGuardian().render()
