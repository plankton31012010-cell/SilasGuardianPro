import streamlit as st
import os
import time
import random
import socket

# --- KONFIGURATION ---
st.set_page_config(page_title="SilasGuardian", page_icon="🛡️", layout="wide")
SAVE_DIR = "sector_3_vault"
if not os.path.exists(SAVE_DIR): os.makedirs(SAVE_DIR)

class SilasGuardian:
    def __init__(self):
        if 'auth_level' not in st.session_state: st.session_state.auth_level = "A0"
        if 'page' not in st.session_state: st.session_state.page = "login"
        if 'system_crash' not in st.session_state: st.session_state.system_crash = False

    def logout(self):
        for key in st.session_state.keys(): st.session_state[key] = None
        st.session_state.auth_level = "A0"
        st.session_state.page = "login"
        st.session_state.system_crash = False
        st.rerun()

    def render(self):
        # --- SPEKTAKULÄRER SYSTEM-ABSTURZ ---
        if st.session_state.system_crash:
            st.markdown("""
                <style>
                @keyframes flicker { 0% { opacity: 0.8; } 5% { opacity: 0.1; } 10% { opacity: 0.9; } 100% { opacity: 1; } }
                .main { background-color: #050000 !important; color: #ff0000 !important; font-family: 'Courier New'; animation: flicker 0.2s infinite; }
                .stButton>button { background: transparent; border: none; color: transparent; height: 1px; width: 1px; }
                .stButton>button:hover { color: #111; }
                </style>
                """, unsafe_allow_html=True)
            
            st.title("☣️ CRITICAL_CORE_CORRUPTION_DETECTED")
            st.write("---" * 20)
            st.error("EMERGENCY LOCKDOWN INITIATED")
            
            # Die getarnte Nachricht
            st.markdown(f"""
            `[DEBUG_LOG_0x{random.randint(1000,9999)}A]`  
            Memory at segment **ALPHA-7** is bleeding into Sektor Zero.  
            All data in Sektor 3 is being overwritten with zeros.  
            If this was an accident, contact the administrator.  
            To attempt a **recovery** of the kernel, the user must **reset** the power supply.  
            `ERROR_CODE: 0x000005FF`
            """)
            
            # Versteckter Reset: Ein Button, der wie normaler Text aussieht
            if st.button("reset"): # Dieser Button ist fast unsichtbar (siehe CSS oben)
                self.logout()
            return

        # --- LOGIN ---
        if st.session_state.auth_level == "A0":
            st.title("🛡️ SilasGuardian | LOGIN")
            col1, col2 = st.columns(2)
            ident = col1.text_input("Ident", type="password")
            pwd = col2.text_input("Sektor-Passwort", type="password")
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
            if st.button("🚨 SHUTDOWN", type="primary"): self.logout()

        # --- SCANNER (REPARIERT) ---
        elif st.session_state.page == "scanner":
            st.title("📡 Live-Netzwerk-Scanner")
            if st.button("← Zurück"): st.session_state.page = "dashboard"; st.rerun()
            
            if st.button("Intensiv-Scan starten"):
                try:
                    target = socket.gethostbyname(socket.gethostname())
                    st.write(f"Scanne lokale Schnittstelle: **{target}**")
                    # Port-Check Logik
                    ports = [21, 22, 80, 443, 3389, 8080]
                    results = []
                    for port in ports:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(0.1)
                        if s.connect_ex((target, port)) == 0:
                            results.append({"Port": port, "Status": "OFFEN"})
                        s.close()
                    if results: st.table(results)
                    else: st.info("Keine offenen Ports gefunden. Stealth-Modus aktiv.")
                except: st.error("Netzwerk-Interface blockiert.")

        # --- SEKTOR 3 (VAULT) ---
        elif st.session_state.page == "vault":
            st.title("📂 Sektor 3")
            if st.button("← Zurück"): st.session_state.page = "dashboard"; st.rerun()
            up = st.file_uploader("Upload")
            if up:
                with open(os.path.join(SAVE_DIR, up.name), "wb") as f: f.write(up.getbuffer())
                st.success("Datei gesichert.")
            for f in os.listdir(SAVE_DIR):
                with open(os.path.join(SAVE_DIR, f), "rb") as fb:
                    st.download_button(f"🔒 {f}", data=fb, file_name=f)

        # --- SEKTOR ZERO (DER ÜBERFALL) ---
        elif st.session_state.page == "honeypot":
            st.title("🛡️ Sektor Zero")
            if st.button("← Zurück"): st.session_state.page = "dashboard"; st.rerun()
            st.error("ACHTUNG: Sektor Zero steuert die Selbstzerstörung.")
            if st.toggle("ACTIVATE OVERRIDE"):
                st.session_state.system_crash = True
                st.rerun()

# --- START ---
if __name__ == "__main__": SilasGuardian().render()
