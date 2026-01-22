import streamlit as st
import os
import time
import datetime
import pandas as pd
import random

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
        if 'crash' not in st.session_state: st.session_state.crash = False
        if 'blackout' not in st.session_state: st.session_state.blackout = False

    def reset_system(self):
        st.session_state.update({
            "crash": False, "blackout": False, "auth_level": "A0", 
            "login_time": None, "scan_status": "idle"
        })
        st.rerun()

    def render(self):
        # Dark-Mode Styling
        st.markdown("<style>.stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New'; }</style>", unsafe_allow_html=True)

        # --- PHASE 3: BLACKOUT (DIE FALLE) ---
        if st.session_state.blackout:
            st.markdown("<style>.main { background-color: #000 !important; cursor: none !important; }</style>", unsafe_allow_html=True)
            if st.button(" ", key="hidden_reset"): self.reset_system()
            return

        # --- PHASE 2: SEKTOR ZERO CRASH ---
        if st.session_state.crash:
            st.title("☣️ SYSTEM_HALTED")
            st.write("CRITICAL ERROR IN SECTOR_0")
            c1, c2, c3, c4 = st.columns(4)
            with c1: 
                if st.button("0x0B12"): st.session_state.blackout = True; st.rerun()
            with c2: 
                if st.button("0xC991"): st.session_state.blackout = True; st.rerun()
            with c3: 
                if st.button("0xAF32"): self.reset_system() # Echter Reset
            with c4: 
                if st.button("0x82FF"): st.session_state.blackout = True; st.rerun()
            return

        # --- PHASE 1: LOGIN (JETZT STABIL) ---
        if st.session_state.auth_level == "A0":
            st.title("🛡️ SilasGuardian Login")
            ident = st.text_input("Ident", type="password", key="login_ident")
            pwd = st.text_input("Sektor-Passwort", type="password", key="login_pwd")
            if st.button("Boot System"):
                if ident.lower() == "silas" and pwd.lower() == "data":
                    st.session_state.auth_level = "A1+"
                    st.session_state.login_time = time.time()
                    st.rerun()
                else:
                    st.error("Zugriff verweigert.")
            return

        # --- DYNAMISCHE BEGRÜSSUNG (Nur nach Login) ---
        elapsed = time.time() - st.session_state.login_time
        if elapsed < 10:
            st.title("Willkommen Anton")
            st.caption(f"System-Vollzugriff aktiv... Banner-Timeout: {10 - int(elapsed)}s")
            time.sleep(1)
            st.rerun()
        else:
            st.title("🛡️ SilasGuardian | Core-Terminal")

        # --- MODULE ---
        tabs = st.tabs(["📡 Scanner", "📂 Vault", "💬 Bridge", "🛡️ Sektor Zero"])

        with tabs[0]: # Scanner
            st.subheader("📡 Deep-Net-Inspector")
            if st.button("Scan starten"):
                st.session_state.scan_status = "running"
                pb = st.progress(0)
                for i in range(100):
                    time.sleep(0.02)
                    pb.progress(i + 1)
                st.session_state.scan_status = "complete"
            
            if st.session_state.scan_status == "complete":
                st.table(pd.DataFrame([
                    {"IP": "192.168.1.1", "Gerät": "FritzBox", "Status": "Online"},
                    {"IP": "192.168.1.42", "Gerät": "iPhone", "Status": "Online"}
                ]))

        with tabs[1]: # Vault
            st.subheader("📂 Sektor 3: Vault")
            up = st.file_uploader("Datei sichern")
            if up:
                with open(os.path.join(VAULT_PATH, up.name), "wb") as f: f.write(up.getbuffer())
            
            for f_name in os.listdir(VAULT_PATH):
                with open(os.path.join(VAULT_PATH, f_name), "rb") as fb:
                    st.download_button(label=f"🔓 {f_name} öffnen", data=fb, file_name=f_name, key=f_name)

        with tabs[2]: # Bridge
            st.subheader("💬 Comms-Bridge")
            msg = st.text_input("Nachricht...")
            if st.button("Senden"):
                st.session_state.chat_log.append(f"[{datetime.datetime.now().strftime('%H:%M')}] Anton: {msg}")
            for chat in reversed(st.session_state.chat_log):
                st.code(chat)

        with tabs[3]: # Sektor Zero
            st.subheader("🛡️ Sektor Zero")
            st.warning("Gefahrenbereich: Modus schaltet das System in den Täuschungs-Crash.")
            if st.toggle("ACTIVATE PANIC MODE"):
                st.session_state.crash = True
                st.rerun()
            st.divider()
            if st.button("🚨 System Showdown (A0)"):
                self.reset_system()

if __name__ == "__main__":
    SilasGuardian().render()
