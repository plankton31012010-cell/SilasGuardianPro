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
        # --- DAS MINENFELD IM ABSTURZ ---
        if st.session_state.crash:
            st.markdown("""
                <style>
                .main { background-color: #010a01 !important; color: #00FF00 !important; font-family: 'Courier New'; }
                .stButton > button { 
                    background: transparent !important; border: none !important; color: #005500 !important; 
                    font-family: 'Courier New' !important; font-size: 14px !important; margin: 0; padding: 0;
                }
                .stButton > button:hover { color: #00FF00 !important; cursor: help; }
                </style>
                """, unsafe_allow_html=True)
            
            st.title("CRITICAL_MEMORY_CORRUPTION")
            st.write("---" * 20)
            st.write("SYSTEM_HALT: STACK_OVERFLOW_DETECTED")
            st.write("Current Memory Dumps (Interactive Debugger):")
            st.write("")

            # Erstellung der Button-Matrix (Das Minenfeld)
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("0x0012"): st.toast("Memory Leak increased...") # Fake
            with col2:
                if st.button("0xC119"): st.toast("Buffer Overflow...") # Fake
            with col3:
                # DAS IST DER ECHTE RESET-PUNKT
                if st.button("0xAF32"): self.recovery() 
            with col4:
                if st.button("0x88FF"): st.toast("Access Denied.") # Fake

            st.write("")
            st.code(f"THREAD_ID: {random.randint(1000, 9999)} | PTR: 0xAF32 (RECOVERY_BIT_LOCKED)", language="bash")
            st.write("Click on the specific memory register to attempt manual re-initialization.")
            return

        # --- LOGIN-SEQUENZ ---
        if st.session_state.auth_level == "A0":
            st.title("🛡️ SilasGuardian")
            ident = st.text_input("Ident-Key", type="password")
            pwd = st.text_input("Sektor-Passwort", type="password")
            if st.button("Boot System"):
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
            if st.button("🚨 TOTAL SHUTDOWN"): self.recovery()

        # --- SEKTOR 3 ---
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

        # --- SEKTOR ZERO ---
        elif st.session_state.page == "honeypot":
            st.title("🛡️ Sektor Zero")
            if st.button("← Dashboard"): st.session_state.page = "dashboard"; st.rerun()
            if st.toggle("PANIC MODE AKTIVIEREN"):
                st.session_state.crash = True; st.rerun()

        # --- SCANNER ---
        elif st.session_state.page == "scanner":
            st.title("📡 Scanner")
            if st.button("← Dashboard"): st.session_state.page = "dashboard"; st.rerun()
            st.write("Schnittstellenprüfung läuft...")

if __name__ == "__main__": SilasGuardian().render()
