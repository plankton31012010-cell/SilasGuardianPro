import streamlit as st
import os
import time
import random

# --- SYSTEM-SETUP ---
st.set_page_config(page_title="SilasGuardian", page_icon="🛡️", layout="wide")
VAULT_PATH = "sector_3_vault"
if not os.path.exists(VAULT_PATH): os.makedirs(VAULT_PATH)

class SilasGuardian:
    def __init__(self):
        if 'auth_level' not in st.session_state: st.session_state.auth_level = "A0"
        if 'page' not in st.session_state: st.session_state.page = "login"
        if 'crash' not in st.session_state: st.session_state.crash = False

    def recovery(self):
        st.session_state.crash = False
        st.session_state.auth_level = "A0"
        st.session_state.page = "login"
        st.rerun()

    def render(self):
        # --- DER ULTIMATIVE GETARNTE ABSTURZ ---
        if st.session_state.crash:
            st.markdown("""
                <style>
                @keyframes crt { 0% { opacity: 0.9; } 50% { opacity: 1; } 100% { opacity: 0.9; } }
                .main { background-color: #020000 !important; color: #00FF00 !important; font-family: 'Courier New'; animation: crt 0.1s infinite; }
                .stButton > button { 
                    background: transparent !important; border: none !important; color: #00FF00 !important; 
                    font-family: 'Courier New' !important; font-size: 14px !important; padding: 0 !important; 
                    margin: 0 !important; height: auto !important; width: auto !important; cursor: default !important;
                }
                .stButton > button:active { background: transparent !important; color: #00FF00 !important; }
                </style>
                """, unsafe_allow_html=True)
            
            st.title("FATAL_EXCEPTION_0x00E44")
            st.write("A critical error has occurred and the system has been halted to prevent data loss.")
            st.write("---" * 20)
            st.write("KERNEL_THREAD_PANIC: SECTOR_ZERO_OVERWRITE")
            st.write("Dumping physical memory to disk: 100%")
            st.write("Contact your system administrator if this problem persists.")
            st.write("")
            
            # GETARNTER RESET: Er sieht aus wie eine technische Zeile
            col1, col2 = st.columns([1, 10])
            with col1:
                # Nur dieser kleine Teil ist der Button!
                if st.button(f"0x{random.randint(4000, 9999)}A"):
                    self.recovery()
            with col2:
                st.write("  <-- STACK_ADDR_RECOVERY_POINT")
            
            st.code(f"REGISTER_DUMP: EAX={random.getrandbits(32)} EBX={random.getrandbits(32)}", language="bash")
            return

        # --- LOGIN ---
        if st.session_state.auth_level == "A0":
            st.title("🛡️ SilasGuardian")
            ident = st.text_input("Ident-Key", type="password")
            pwd = st.text_input("Sektor-Passwort", type="password")
            if st.button("Initialisieren"):
                if ident.lower() == "silas" and pwd.lower() == "data":
                    st.session_state.auth_level = "A1+"; st.session_state.page = "dashboard"; st.rerun()
            return

        # --- DASHBOARD (ANTON) ---
        if st.session_state.page == "dashboard":
            st.title("Hallo Anton")
            st.subheader("Systemstatus: A1+ Vollzugriff")
            c1, c2, c3 = st.columns(3)
            if c1.button("📡 Scanner"): st.session_state.page = "scanner"; st.rerun()
            if c2.button("📂 Sektor 3"): st.session_state.page = "vault"; st.rerun()
            if c3.button("🛡️ Sektor Zero"): st.session_state.page = "honeypot"; st.rerun()
            st.divider()
            if st.button("🚨 SHUTDOWN"): self.recovery()

        # --- SEKTOR 3 (VAULT) ---
        elif st.session_state.page == "vault":
            st.title("📂 Sektor 3 - Vault")
            if st.button("← Dashboard"): st.session_state.page = "dashboard"; st.rerun()
            up = st.file_uploader("Datei sichern")
            if up:
                with open(os.path.join(VAULT_PATH, up.name), "wb") as f: f.write(up.getbuffer())
                st.success("Datei gespeichert.")
            for f in os.listdir(VAULT_PATH):
                with open(os.path.join(VAULT_PATH, f), "rb") as fd:
                    st.download_button(f"🔓 {f}", data=fd, file_name=f, key=f)

        # --- SEKTOR ZERO (HONEYPOT) ---
        elif st.session_state.page == "honeypot":
            st.title("🛡️ Sektor Zero")
            if st.button("← Dashboard"): st.session_state.page = "dashboard"; st.rerun()
            if st.toggle("NOTFALL-ABSTURZ AKTIVIEREN"):
                st.session_state.crash = True
                st.rerun()

        # --- SCANNER ---
        elif st.session_state.page == "scanner":
            st.title("📡 Scanner")
            if st.button("← Dashboard"): st.session_state.page = "dashboard"; st.rerun()
            st.write("Scan läuft...")
            time.sleep(1)
            st.success("Netzwerk sauber.")

if __name__ == "__main__": SilasGuardian().render()
