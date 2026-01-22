import streamlit as st
import os
import time
import random
import socket

# --- SYSTEM-SETUP ---
st.set_page_config(page_title="SilasGuardian", page_icon="🛡️", layout="wide")
VAULT_PATH = "sector_3_vault"
if not os.path.exists(VAULT_PATH):
    os.makedirs(VAULT_PATH)

class SilasGuardian:
    def __init__(self):
        if 'auth_level' not in st.session_state: st.session_state.auth_level = "A0"
        if 'page' not in st.session_state: st.session_state.page = "login"
        if 'system_crash' not in st.session_state: st.session_state.system_crash = False

    def trigger_reset(self):
        st.session_state.system_crash = False
        st.session_state.auth_level = "A0"
        st.session_state.page = "login"
        st.rerun()

    def render(self):
        # --- DER SPEKTAKULÄRE ABSTURZ (SEKTOR ZERO) ---
        if st.session_state.system_crash:
            st.markdown("""
                <style>
                @keyframes shake { 0% { transform: translate(1px, 1px) rotate(0deg); } 10% { transform: translate(-1px, -2px) rotate(-1deg); } 100% { transform: translate(1px, -2px) rotate(-1deg); } }
                .main { background-color: #050000 !important; color: #ff3333 !important; animation: shake 0.5s infinite; }
                .hidden-btn { background: none; border: none; color: #ff3333; text-decoration: underline; cursor: pointer; font-family: 'Courier New'; padding: 0; font-size: 16px; }
                </style>
                """, unsafe_allow_html=True)
            
            st.title("☣️ CRITICAL_CORE_CORRUPTION_DETECTED")
            st.error("EMERGENCY LOCKDOWN INITIATED")
            st.write("---" * 15)
            st.write("Memory at segment ALPHA-7 is bleeding into Sektor Zero.")
            st.write("All data in Sektor 3 is being overwritten with zeros.")
            
            # Der getarnte Reset-Link
            st.write("To attempt a recovery of the kernel, the user must:")
            if st.button("reset the power supply", key="secret_reset"):
                self.trigger_reset()
            
            st.code(f"ERROR_CODE: 0x00000{random.randint(100,999)}FF", language="bash")
            return

        # --- NORMALER LOGIN ---
        if st.session_state.auth_level == "A0":
            st.title("🛡️ SilasGuardian | BOOT_SEQUENCE")
            ident = st.text_input("Ident-Key", type="password")
            pwd = st.text_input("Sektor-Passwort", type="password")
            if st.button("Starten"):
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
            if st.button("🚨 SHUTDOWN"): self.trigger_reset()

        # --- SCANNER ---
        elif st.session_state.page == "scanner":
            st.title("📡 Netzwerk-Integrität")
            if st.button("← Zurück"): st.session_state.page = "dashboard"; st.rerun()
            if st.button("Scan starten"):
                with st.spinner("Scanne lokale Schnittstellen..."):
                    time.sleep(1)
                    st.success("Schnittstelle 127.0.0.1 aktiv. Keine externen Eindringlinge gefunden.")

        # --- SEKTOR 3 (VAULT) ---
        elif st.session_state.page == "vault":
            st.title("📂 Sektor 3 - Vault")
            if st.button("← Zurück"): st.session_state.page = "dashboard"; st.rerun()
            up = st.file_uploader("Datei sichern")
            if up:
                with open(os.path.join(VAULT_PATH, up.name), "wb") as f:
                    f.write(up.getbuffer())
                st.success("Datei physikalisch gespeichert.")
            
            st.write("### Archivierte Daten:")
            for f in os.listdir(VAULT_PATH):
                with open(os.path.join(VAULT_PATH, f), "rb") as file_data:
                    st.download_button(f"📄 {f} extrahieren", data=file_data, file_name=f)

        # --- SEKTOR ZERO ---
        elif st.session_state.page == "honeypot":
            st.title("🛡️ Sektor Zero")
            if st.button("← Zurück"): st.session_state.page = "dashboard"; st.rerun()
            if st.toggle("ACTIVATE EMERGENCY SELF-DESTRUCT"):
                st.session_state.system_crash = True
                st.rerun()

if __name__ == "__main__":
    SilasGuardian().render()
