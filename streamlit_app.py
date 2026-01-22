import streamlit as st
import os
import time
import random
import socket
import datetime
import pandas as pd

# --- SYSTEM-KONFIGURATION ---
st.set_page_config(page_title="SilasGuardian", page_icon="🛡️", layout="wide")
VAULT_PATH = "sector_3_vault"
INTRUDER_LOG = "intruder_log.txt"
if not os.path.exists(VAULT_PATH): os.makedirs(VAULT_PATH)

class SilasGuardian:
    def __init__(self):
        # Bestehende Zustände
        if 'auth_level' not in st.session_state: st.session_state.auth_level = "A0"
        if 'page' not in st.session_state: st.session_state.page = "dashboard"
        if 'crash' not in st.session_state: st.session_state.crash = False
        if 'blackout' not in st.session_state: st.session_state.blackout = False
        # Neue Zustände für die 5 Funktionen
        if 'last_action' not in st.session_state: st.session_state.last_action = time.time()
        if 'chat_log' not in st.session_state: st.session_state.chat_log = []

    def log_intruder(self, code):
        """Funktion 2: Intruder-Log"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] ALARM: Falscher Code {code} eingegeben. Blackout ausgelöst.\n"
        with open(os.path.join(VAULT_PATH, INTRUDER_LOG), "a") as f:
            f.write(entry)

    def recovery(self):
        st.session_state.update({"crash": False, "blackout": False, "auth_level": "A0", "page": "login"})
        st.rerun()

    def check_autolock(self):
        """Funktion 4: Auto-Lock (Timeout nach 10 Min)"""
        if st.session_state.auth_level != "A0":
            if time.time() - st.session_state.last_action > 600: # 600 Sek = 10 Min
                self.recovery()

    def render(self):
        self.check_autolock()
        
        # --- FUNKTION 5: DARK-MODE INTERFACE (CSS) ---
        st.markdown("""
            <style>
            .stApp { background-color: #0a0a0a; color: #00ff41; }
            .stButton>button { border: 1px solid #00ff41; background-color: #001500; color: #00ff41; }
            .stButton>button:hover { background-color: #00ff41; color: #000; box-shadow: 0 0 10px #00ff41; }
            </style>
            """, unsafe_allow_html=True)

        # --- BLACKOUT-FALLE ---
        if st.session_state.blackout:
            st.markdown("<style>.main { background-color: #000 !important; cursor: none !important; }</style>", unsafe_allow_html=True)
            if st.button(" ", key="hidden_reset"): self.recovery()
            return

        # --- CRASH-MODUS ---
        if st.session_state.crash:
            st.title("☣️ SYSTEM_HALTED")
            c1, c2, c3, c4 = st.columns(4)
            if c1.button("0x0B12"): self.log_intruder("0x0B12"); st.session_state.blackout = True; st.rerun()
            if c2.button("0xC991"): self.log_intruder("0xC991"); st.session_state.blackout = True; st.rerun()
            if c3.button("0xAF32"): self.recovery() # Echter Reset
            if c4.button("0x82FF"): self.log_intruder("0x82FF"); st.session_state.blackout = True; st.rerun()
            return

        # --- LOGIN ---
        if st.session_state.auth_level == "A0":
            st.title("🛡️ SilasGuardian | Terminal Login")
            ident = st.text_input("Ident", type="password")
            pwd = st.text_input("Password", type="password")
            if st.button("Boot"):
                if ident.lower() == "silas" and pwd.lower() == "data":
                    st.session_state.auth_level = "A1+"; st.rerun()
            return

        # --- DASHBOARD ---
        st.session_state.last_action = time.time() # Reset Timeout
        if st.session_state.page == "dashboard":
            st.title(f"Willkommen, Anton")
            st.write(f"Systemzeit: {datetime.datetime.now().strftime('%H:%M:%S')}")
            
            tabs = st.tabs(["📊 Status", "📡 Scanner", "📂 Vault", "🛡️ Sektor Zero", "💬 Bridge"])
            
            with tabs[0]: # Dashboard / Status
                st.subheader("System-Metriken")
                st.metric("Sicherheitsebene", "A1+")
                st.metric("Vault-Integrität", "Verschlüsselt")
                if st.button("🚨 NOT-AUS", type="primary"): self.recovery()

            with tabs[1]: # Funktion 1: Deep-Net-Inspector
                st.subheader("📡 Deep-Net-Inspector")
                if st.button("Deep Scan starten"):
                    with st.spinner("Identifiziere Geräte-Signaturen..."):
                        time.sleep(2)
                        scan_data = [
                            {"IP": "192.168.1.1", "Gerät": "FritzBox 7590", "Typ": "Gateway"},
                            {"IP": "192.168.1.42", "Gerät": "Apple iPhone 15", "Typ": "Mobile"},
                            {"IP": "192.168.1.102", "Gerät": "Samsung SmartTV", "Typ": "IoT"}
                        ]
                        st.table(pd.DataFrame(scan_data))

            with tabs[2]: # Sektor 3 / Vault & Intruder Log
                st.subheader("📂 Sektor 3 (Vault)")
                up = st.file_uploader("Upload")
                if up:
                    with open(os.path.join(VAULT_PATH, up.name), "wb") as f: f.write(up.getbuffer())
                
                if st.checkbox("Zeige Intruder-Logs (Funktion 2)"):
                    if os.path.exists(os.path.join(VAULT_PATH, INTRUDER_LOG)):
                        with open(os.path.join(VAULT_PATH, INTRUDER_LOG), "r") as f:
                            st.text(f.read())

            with tabs[3]: # Sektor Zero / Panic
                st.subheader("🛡️ Sektor Zero")
                if st.toggle("PANIC MODE AKTIVIEREN"):
                    st.session_state.crash = True; st.rerun()

            with tabs[4]: # Funktion 3: Verschlüsselter Chat
                st.subheader("💬 Bridge (Verschlüsselter Chat)")
                msg = st.text_input("Nachricht eingeben")
                if st.button("Senden"):
                    st.session_state.chat_log.append(f"{datetime.datetime.now().strftime('%H:%M')}: {msg}")
                for log in reversed(st.session_state.chat_log):
                    st.write(f"🔒 {log}")

if __name__ == "__main__":
    SilasGuardian().render()
