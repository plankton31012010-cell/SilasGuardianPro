import streamlit as st
import os
import time
import datetime
import pandas as pd

# --- SYSTEM-SETUP ---
st.set_page_config(page_title="SilasGuardian", page_icon="🛡️", layout="wide")
VAULT_PATH = "sector_3_vault"
LOG_FILE = os.path.join(VAULT_PATH, "intruder_log.txt")
BRIDGE_FILE = os.path.join(VAULT_PATH, "bridge_logs.txt")

if not os.path.exists(VAULT_PATH): os.makedirs(VAULT_PATH)

class SilasGuardian:
    def __init__(self):
        if 'auth_level' not in st.session_state: st.session_state.auth_level = "A0"
        if 'login_time' not in st.session_state: st.session_state.login_time = None
        # WICHTIG: Status-Speicher für den Scanner
        if 'scan_result_ready' not in st.session_state: st.session_state.scan_result_ready = False
        if 'chat_log' not in st.session_state: st.session_state.chat_log = []
        if 'crash' not in st.session_state: st.session_state.crash = False
        if 'blackout' not in st.session_state: st.session_state.blackout = False

    def write_log(self, filename, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(filename, "a") as f:
            f.write(f"[{timestamp}] {message}\n")

    def reset_system(self):
        st.session_state.update({
            "crash": False, "blackout": False, "auth_level": "A0", 
            "login_time": None, "scan_result_ready": False
        })
        st.rerun()

    def render(self):
        st.markdown("<style>.stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New'; }</style>", unsafe_allow_html=True)

        # --- CRASH & BLACKOUT LOGIK ---
        if st.session_state.blackout:
            st.markdown("<style>.main { background-color: #000 !important; }</style>", unsafe_allow_html=True)
            if st.button(" ", key="hidden_reset"): self.reset_system()
            return

        if st.session_state.crash:
            st.title("☣️ SYSTEM_HALTED")
            cols = st.columns(4)
            if cols[0].button("0x0B12"): self.write_log(LOG_FILE, "ALARM: 0x0B12"); st.session_state.blackout = True; st.rerun()
            if cols[1].button("0xC991"): self.write_log(LOG_FILE, "ALARM: 0xC991"); st.session_state.blackout = True; st.rerun()
            if cols[2].button("0xAF32"): self.reset_system()
            if cols[3].button("0x82FF"): self.write_log(LOG_FILE, "ALARM: 0x82FF"); st.session_state.blackout = True; st.rerun()
            return

        # --- LOGIN ---
        if st.session_state.auth_level == "A0":
            st.title("🛡️ SilasGuardian Login")
            ident = st.text_input("Ident", type="password")
            pwd = st.text_input("Passwort", type="password")
            if st.button("Boot"):
                if ident.lower() == "silas" and pwd.lower() == "data":
                    st.session_state.auth_level = "A1+"
                    st.session_state.login_time = time.time()
                    st.rerun()
            return

        # --- TIMER (5s) ---
        elapsed = time.time() - st.session_state.login_time
        if elapsed < 5:
            st.title("Willkommen Anton")
            st.caption(f"Initialisierung... {5 - int(elapsed)}s")
            time.sleep(1); st.rerun()
        else:
            st.title("🛡️ SilasGuardian | Terminal")

        tabs = st.tabs(["📡 Scanner", "📂 Sektor 3", "💬 Bridge", "🛡️ Sektor Zero"])

        # --- 1. SCANNER (FIXED) ---
        with tabs[0]:
            st.subheader("📡 Deep-Net-Inspector")
            
            # Button zum Starten oder Zurücksetzen
            if st.button("Deep Scan starten"):
                st.session_state.scan_result_ready = False # Alten Scan löschen
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i in range(100):
                    time.sleep(0.02)
                    progress_bar.progress(i + 1)
                    status_text.text(f"Scanne Frequenzen... {i+1}%")
                
                st.session_state.scan_result_ready = True # Status auf "Fertig" setzen
                st.rerun() # Seite neu laden um Tabelle anzuzeigen

            # Anzeige der Ergebnisse wenn Status "Fertig"
            if st.session_state.scan_result_ready:
                st.success("✅ Netzwerk-Integrität geprüft. Ergebnisse dechiffriert:")
                scan_data = [
                    {"IP": "192.168.1.1", "Gerät": "FritzBox 7590", "MAC": "00:E0:4C:53:12:01", "Status": "Aktiv"},
                    {"IP": "192.168.1.42", "Gerät": "Apple iPhone 15", "MAC": "7C:D1:C3:94:02:88", "Status": "Aktiv"},
                    {"IP": "192.168.1.105", "Gerät": "Sony PlayStation 5", "MAC": "44:F4:11:00:AA:BB", "Status": "Standby"}
                ]
                st.table(pd.DataFrame(scan_data))
                if st.button("Ergebnisse löschen"):
                    st.session_state.scan_result_ready = False
                    st.rerun()

        # --- 2. SEKTOR 3 (VAULT) ---
        with tabs[1]:
            st.subheader("📂 Sektor 3 - Vault")
            if st.checkbox("Logs einsehen"):
                if os.path.exists(LOG_FILE):
                    with open(LOG_FILE, "r") as f: st.text_area("Intruder Logs", f.read(), height=150)
                if os.path.exists(BRIDGE_FILE):
                    with open(BRIDGE_FILE, "r") as f: st.text_area("Bridge Archiv", f.read(), height=150)
            
            st.divider()
            up = st.file_uploader("Datei hochladen")
            if up:
                with open(os.path.join(VAULT_PATH, up.name), "wb") as f: f.write(up.getbuffer())
            
            for f_name in os.listdir(VAULT_PATH):
                if f_name not in ["intruder_log.txt", "bridge_logs.txt"]:
                    with open(os.path.join(VAULT_PATH, f_name), "rb") as fb:
                        st.download_button(f"🔓 {f_name} öffnen", fb, file_name=f_name, key=f_name)

        # --- 3. BRIDGE (PERSISTENT) ---
        with tabs[2]:
            st.subheader("💬 Comms-Bridge")
            new_msg = st.text_input("Nachricht...")
            if st.button("Senden"):
                if new_msg:
                    self.write_log(BRIDGE_FILE, f"Anton: {new_msg}")
                    st.rerun()
            
            if os.path.exists(BRIDGE_FILE):
                with open(BRIDGE_FILE, "r") as f:
                    for line in reversed(f.readlines()):
                        st.code(line.strip())

        # --- 4. SEKTOR ZERO ---
        with tabs[3]:
            if st.toggle("PANIC MODE"): st.session_state.crash = True; st.rerun()
            if st.button("🚨 Shutdown"): self.reset_system()

if __name__ == "__main__":
    SilasGuardian().render()
