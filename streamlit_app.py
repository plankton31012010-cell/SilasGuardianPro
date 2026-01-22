import streamlit as st
import os
import time
import datetime
import pandas as pd

# --- SYSTEM-SETUP ---
st.set_page_config(page_title="SilasGuardian", page_icon="🛡️", layout="wide")
VAULT_PATH = "sector_3_vault"
LOG_FILE = os.path.join(VAULT_PATH, "intruder_log.txt")
BRIDGE_FILE = os.path.join(VAULT_PATH, "bridge_logs.txt") # Neue Speicherdatei

if not os.path.exists(VAULT_PATH): os.makedirs(VAULT_PATH)

class SilasGuardian:
    def __init__(self):
        if 'auth_level' not in st.session_state: st.session_state.auth_level = "A0"
        if 'login_time' not in st.session_state: st.session_state.login_time = None
        if 'scan_status' not in st.session_state: st.session_state.scan_status = "idle"
        if 'crash' not in st.session_state: st.session_state.crash = False
        if 'blackout' not in st.session_state: st.session_state.blackout = False

    def write_log(self, filename, message):
        """Universelle Speicherfunktion für Logs und Bridge"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(filename, "a") as f:
            f.write(f"[{timestamp}] {message}\n")

    def load_bridge(self):
        """Lädt die Chat-Historie aus der Datei"""
        if os.path.exists(BRIDGE_FILE):
            with open(BRIDGE_FILE, "r") as f:
                return f.readlines()
        return []

    def reset_system(self):
        st.session_state.update({"crash": False, "blackout": False, "auth_level": "A0", "login_time": None})
        st.rerun()

    def render(self):
        st.markdown("<style>.stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New'; }</style>", unsafe_allow_html=True)

        # --- BLACKOUT & CRASH LOGIK (Unverändert stabil) ---
        if st.session_state.blackout:
            st.markdown("<style>.main { background-color: #000 !important; }</style>", unsafe_allow_html=True)
            if st.button(" ", key="hidden_reset"): self.reset_system()
            return

        if st.session_state.crash:
            st.title("☣️ SYSTEM_HALTED")
            cols = st.columns(4)
            if cols[0].button("0x0B12"): self.write_log(LOG_FILE, "ALARM: Code 0x0B12"); st.session_state.blackout = True; st.rerun()
            if cols[1].button("0xC991"): self.write_log(LOG_FILE, "ALARM: Code 0xC991"); st.session_state.blackout = True; st.rerun()
            if cols[2].button("0xAF32"): self.reset_system()
            if cols[3].button("0x82FF"): self.write_log(LOG_FILE, "ALARM: Code 0x82FF"); st.session_state.blackout = True; st.rerun()
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

        # 1. SCANNER (Unverändert)
        with tabs[0]:
            if st.button("Deep Scan"):
                st.session_state.scan_status = "running"
                pb = st.progress(0)
                for i in range(100): time.sleep(0.01); pb.progress(i + 1)
                st.session_state.scan_status = "complete"
            if st.session_state.scan_status == "complete":
                st.table(pd.DataFrame([{"IP": "192.168.1.1", "Gerät": "FritzBox", "Status": "Online"}]))

        # 2. SEKTOR 3 (VAULT)
        with tabs[1]:
            st.subheader("📂 Sektor 3 - Vault & Archiv")
            if st.checkbox("System-Protokolle anzeigen"):
                if os.path.exists(LOG_FILE):
                    with open(LOG_FILE, "r") as f: st.text_area("Intruder Logs", f.read(), height=150)
                if os.path.exists(BRIDGE_FILE):
                    with open(BRIDGE_FILE, "r") as f: st.text_area("Bridge Archiv", f.read(), height=150)
            st.divider()
            for f_name in os.listdir(VAULT_PATH):
                if f_name not in ["intruder_log.txt", "bridge_logs.txt"]:
                    with open(os.path.join(VAULT_PATH, f_name), "rb") as fb:
                        st.download_button(f"🔓 {f_name}", fb, file_name=f_name, key=f_name)

        # 3. COMMS-BRIDGE (JETZT PERMANENT)
        with tabs[2]:
            st.subheader("💬 Comms-Bridge (Persistent Memory)")
            new_msg = st.text_input("Neue Nachricht schreiben...")
            if st.button("Absenden"):
                if new_msg:
                    self.write_log(BRIDGE_FILE, f"Anton: {new_msg}")
                    st.rerun() # Seite neu laden um Nachricht sofort anzuzeigen
            
            st.divider()
            history = self.load_bridge()
            if history:
                for line in reversed(history):
                    st.code(line.strip())
            else:
                st.info("Keine Nachrichten im Archiv.")

        # 4. SEKTOR ZERO
        with tabs[3]:
            if st.toggle("PANIC MODE"): st.session_state.crash = True; st.rerun()
            if st.button("🚨 Shutdown"): self.reset_system()

if __name__ == "__main__":
    SilasGuardian().render()
