import streamlit as st
import os
import time
import datetime
import pandas as pd

# --- SYSTEM-SETUP ---
st.set_page_config(page_title="SilasGuardian", page_icon="🛡️", layout="wide")
VAULT_PATH = "sector_3_vault"
LOG_FILE = os.path.join(VAULT_PATH, "intruder_log.txt")
if not os.path.exists(VAULT_PATH): os.makedirs(VAULT_PATH)

class SilasGuardian:
    def __init__(self):
        if 'auth_level' not in st.session_state: st.session_state.auth_level = "A0"
        if 'login_time' not in st.session_state: st.session_state.login_time = None
        if 'scan_status' not in st.session_state: st.session_state.scan_status = "idle"
        if 'chat_log' not in st.session_state: st.session_state.chat_log = []
        if 'crash' not in st.session_state: st.session_state.crash = False
        if 'blackout' not in st.session_state: st.session_state.blackout = False

    def write_log(self, code):
        """Schreibt den Eindringversuch sofort in die Datei in Sektor 3"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a") as f:
            f.write(f"[{timestamp}] CRASH_TRIGGER: Code {code} benutzt. Blackout eingeleitet.\n")

    def reset_system(self):
        st.session_state.update({"crash": False, "blackout": False, "auth_level": "A0", "login_time": None})
        st.rerun()

    def render(self):
        st.markdown("<style>.stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New'; }</style>", unsafe_allow_html=True)

        if st.session_state.blackout:
            st.markdown("<style>.main { background-color: #000 !important; cursor: none !important; }</style>", unsafe_allow_html=True)
            if st.button(" ", key="hidden_reset"): self.reset_system()
            return

        if st.session_state.crash:
            st.title("☣️ SYSTEM_HALTED")
            cols = st.columns(4)
            # Falsche Codes mit Logging-Funktion
            if cols[0].button("0x0B12"): self.write_log("0x0B12"); st.session_state.blackout = True; st.rerun()
            if cols[1].button("0xC991"): self.write_log("0xC991"); st.session_state.blackout = True; st.rerun()
            if cols[2].button("0xAF32"): self.reset_system() # Echter Reset (kein Log nötig)
            if cols[3].button("0x82FF"): self.write_log("0x82FF"); st.session_state.blackout = True; st.rerun()
            return

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

        # --- TIMER: 5 SEKUNDEN ---
        elapsed = time.time() - st.session_state.login_time
        if elapsed < 5:
            st.title("Willkommen Anton")
            st.caption(f"Initialisierung... {5 - int(elapsed)}s")
            time.sleep(1)
            st.rerun()
        else:
            st.title("🛡️ SilasGuardian | Terminal")

        tabs = st.tabs(["📡 Scanner", "📂 Sektor 3", "💬 Bridge", "🛡️ Sektor Zero"])

        with tabs[0]: # Scanner
            if st.button("Deep Scan"):
                st.session_state.scan_status = "running"
                pb = st.progress(0)
                for i in range(100):
                    time.sleep(0.02)
                    pb.progress(i + 1)
                st.session_state.scan_status = "complete"
            if st.session_state.scan_status == "complete":
                st.table(pd.DataFrame([{"IP": "192.168.1.1", "Status": "Online"}]))

        with tabs[1]: # Sektor 3 / Logbuch
            st.subheader("📂 Sektor 3 - Vault & Logs")
            if st.checkbox("Zeige intruder_log.txt"):
                if os.path.exists(LOG_FILE):
                    with open(LOG_FILE, "r") as f:
                        st.text_area("System-Protokoll", f.read(), height=200)
                else: st.info("Keine Einträge vorhanden.")
            
            st.divider()
            for f_name in os.listdir(VAULT_PATH):
                if f_name != "intruder_log.txt":
                    with open(os.path.join(VAULT_PATH, f_name), "rb") as fb:
                        st.download_button(f"🔓 {f_name}", fb, file_name=f_name, key=f_name)

        with tabs[2]: # Chat
            msg = st.text_input("Nachricht...")
            if st.button("Senden"):
                st.session_state.chat_log.append(f"[{datetime.datetime.now().strftime('%H:%M')}] Anton: {msg}")
            for chat in reversed(st.session_state.chat_log): st.code(chat)

        with tabs[3]: # Sektor Zero
            if st.toggle("PANIC MODE"): st.session_state.crash = True; st.rerun()
            if st.button("🚨 Shutdown"): self.reset_system()

if __name__ == "__main__":
    SilasGuardian().render()
