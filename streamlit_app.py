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
        if 'blackout' not in st.session_state: st.session_state.blackout = False

    def recovery(self):
        st.session_state.crash = False
        st.session_state.blackout = False
        st.session_state.auth_level = "A0"
        st.session_state.page = "login"
        st.rerun()

    def trigger_blackout(self):
        st.session_state.blackout = True
        st.rerun()

    def render(self):
        # --- PHASE 2: TOTALER BLACKOUT (DIE FALLE) ---
        if st.session_state.blackout:
            color = random.choice(["#FFFFFF", "#000000"])
            st.markdown(f"""
                <style>
                .main {{ background-color: {color} !important; }}
                * {{ color: {color} !important; cursor: none !important; }}
                #MainMenu, footer, header {{visibility: hidden;}}
                </style>
                """, unsafe_allow_html=True)
            # Versteckter Notfall-Reset (Klick irgendwo oben links reaktiviert es für dich)
            if st.button(" ", key="emergency_reset"):
                self.recovery()
            return

        # --- PHASE 1: DER GETARNTE ABSTURZ ---
        if st.session_state.crash:
            st.markdown("""
                <style>
                .main { background-color: #010501 !important; color: #00FF00 !important; font-family: 'Courier New'; }
                .stButton > button { 
                    background: transparent !important; border: none !important; 
                    color: #008800 !important; font-family: 'Courier New' !important; 
                    font-size: 14px !important; margin: 0; padding: 0; height: 20px;
                }
                .stButton > button:hover { color: #00FF00 !important; border: none !important; }
                .stButton > button:active { background: transparent !important; border: none !important; }
                </style>
                """, unsafe_allow_html=True)
            
            st.title("FATAL_MEMORY_LEAK_DETECTION")
            st.write("---" * 20)
            st.write("CRITICAL: Stack smashing detected at Core_0. System paused.")
            st.write("Local Registers:")
            
            # Die Button-Matrix
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                if st.button("0x0B12"): self.trigger_blackout() # FALLE
            with c2:
                if st.button("0xC991"): self.trigger_blackout() # FALLE
            with c3:
                # ECHTER RESET (DEIN GEHEIMNIS)
                if st.button("0xAF32"): self.recovery() 
            with c4:
                if st.button("0x82FF"): self.trigger_blackout() # FALLE

            st.write("")
            st.code("LOG: Attempting to dump register 0xAF32... [FAILED]", language="bash")
            st.write("System locked. Hardware reboot required.")
            return

        # --- NORMALER LOGIN ---
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
            if st.toggle("ACTIVATE PANIC MODE"):
                st.session_state.crash = True; st.rerun()

        # --- SCANNER ---
        elif st.session_state.page == "scanner":
            st.title("📡 Scanner")
            if st.button("← Dashboard"): st.session_state.page = "dashboard"; st.rerun()
            st.write("Integritätsprüfung aktiv...")

if __name__ == "__main__": SilasGuardian().render()
