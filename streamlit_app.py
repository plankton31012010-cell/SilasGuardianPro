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
        # Hard Reset der Zustände
        st.session_state.crash = False
        st.session_state.auth_level = "A0"
        st.session_state.page = "login"
        st.rerun()

    def render(self):
        # --- DER ULTIMATIVE GETARNTE ABSTURZ ---
        if st.session_state.crash:
            st.markdown("""
                <style>
                .main { background-color: #020000 !important; color: #00FF00 !important; font-family: 'Courier New'; }
                .stButton > button { 
                    background: transparent !important; border: 1px solid #003300 !important; color: #00FF00 !important; 
                    font-family: 'Courier New' !important; font-size: 14px !important; 
                    cursor: crosshair !important;
                }
                .stButton > button:hover { border: 1px solid #00FF00 !important; }
                </style>
                """, unsafe_allow_html=True)
            
            st.title("FATAL_EXCEPTION_0x00E44")
            st.write("---" * 20)
            st.write("KERNEL_THREAD_PANIC: SECTOR_ZERO_OVERWRITE")
            st.write("Dumping physical memory to disk...")
            st.write("")
            
            # GETARNTER RESET: Jetzt stabil in einer Spalte
            col1, col2 = st.columns([1, 5])
            with col1:
                # Wir nehmen eine feste Zahl für diesen Absturz-Zyklus
                if st.button("0x88FF2"):
                    self.recovery()
            with col2:
                st.write(" <-- ADDR_STK_RECOVERY")
            
            st.code("DEBUG_PTR: [C://SYSTEM/ROOT/SILAS_PROT.LOG]", language="bash")
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

        # --- DASHBOARD ---
        if st.session_state.page == "dashboard":
            st.title("Hallo Anton")
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
            st.write("Echtzeit-Analyse aktiv...")
            # Hier kannst du deine Port-Scan Logik wieder einfügen

if __name__ == "__main__": SilasGuardian().render()
