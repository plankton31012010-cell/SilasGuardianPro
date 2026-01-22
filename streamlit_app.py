import streamlit as st
import os
import time
import random

# --- KONFIGURATION & PERSISTENZ ---
st.set_page_config(page_title="SilasGuardian", page_icon="🛡️", layout="wide")
SAVE_DIR = "sector_3_vault"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

class SilasGuardian:
    def __init__(self):
        if 'auth_level' not in st.session_state:
            st.session_state.auth_level = "A0"
        if 'page' not in st.session_state:
            st.session_state.page = "login"
        if 'system_crash' not in st.session_state:
            st.session_state.system_crash = False

    def logout(self):
        st.session_state.auth_level = "A0"
        st.session_state.page = "login"
        st.session_state.system_crash = False
        st.rerun()

    def render(self):
        # --- NOTFALL-PROTOKOLL: SYSTEM ABSTURZ (SEKTOR ZERO) ---
        if st.session_state.system_crash:
            st.markdown("""
                <style>
                .reportview-container { background: black; }
                .main { background: black; color: #00FF00; font-family: 'Courier New', Courier, monospace; }
                </style>
                """, unsafe_allow_html=True)
            st.title("⚠️ FATAL ERROR: SYSTEM HALTED")
            st.code(f"""
            [CRITICAL] Kernel Panic in Sector 0
            [ERROR] Memory Corruption at 0x000{random.randint(1000,9999)}
            [INFO] Encrypting Core Files... 100%
            [SECURITY] Unauthorized access attempt detected. 
            [STATUS] SYSTEM_LOCKED_BY_SILAS_GUARDIAN
            """, language="bash")
            time.sleep(0.5)
            if st.button("RECOVERY MODE"):
                self.logout()
            return

        # --- 1. LOGIN SEITE ---
        if st.session_state.auth_level == "A0":
            st.title("🛡️ SilasGuardian | Systemzugang")
            st.divider()
            col1, col2 = st.columns(2)
            ident = col1.text_input("Ident-Key", type="password")
            pwd = col2.text_input("Sektor-Passwort", type="password")
            
            if st.button("System initialisieren"):
                if ident.lower() == "silas" and pwd.lower() == "data":
                    st.session_state.auth_level = "A1+"
                    st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    st.error("Zugriff verweigert.")
            return

        # --- 2. DASHBOARD ---
        if st.session_state.page == "dashboard":
            st.title("Hallo Anton")
            st.info("Systemstatus: ONLINE (A1+)")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📡 Netzwerk-Scanner", use_container_width=True):
                    st.session_state.page = "scanner"; st.rerun()
            with col2:
                if st.button("📂 Sektor 3 (Vault)", use_container_width=True):
                    st.session_state.page = "vault"; st.rerun()
            with col3:
                if st.button("🛡️ Sektor Zero", use_container_width=True):
                    st.session_state.page = "honeypot"; st.rerun()

            st.divider()
            if st.button("🚨 SYSTEM SHUTDOWN", type="primary", use_container_width=True):
                self.logout()

        # --- 3. SEKTOR 3: VAULT ---
        elif st.session_state.page == "vault":
            st.title("📂 Sektor 3: Sicherer Datentresor")
            if st.button("← Zurück"): st.session_state.page = "dashboard"; st.rerun()
            
            up = st.file_uploader("Datei speichern")
            if up:
                with open(os.path.join(SAVE_DIR, up.name), "wb") as f:
                    f.write(up.getbuffer())
                st.success(f"'{up.name}' archiviert.")

            files = os.listdir(SAVE_DIR)
            for f in files:
                with open(os.path.join(SAVE_DIR, f), "rb") as fb:
                    st.download_button(f"🔒 {f} öffnen", data=fb, file_name=f, key=f)

        # --- 4. SEKTOR ZERO: HONEY-POT & CRASH ---
        elif st.session_state.page == "honeypot":
            st.title("🛡️ Sektor Zero: Sicherheits-Override")
            if st.button("← Zurück"): st.session_state.page = "dashboard"; st.rerun()
            
            st.warning("VORSICHT: Die Aktivierung des Honey-Pots löst eine System-Verschlüsselung aus.")
            if st.toggle("PANIC MODE: System-Absturz simulieren"):
                st.session_state.system_crash = True
                st.rerun()

# --- START ---
if __name__ == "__main__":
    SilasGuardian().render()
