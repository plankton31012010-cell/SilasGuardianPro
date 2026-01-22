import streamlit as st
import os
import time
import datetime
import pandas as pd
import random
import plotly.express as px

# --- SYSTEM-SETUP ---
st.set_page_config(page_title="SilasGuardian", page_icon="🛡️", layout="wide")
VAULT_PATH = "sector_3_vault"
LOG_FILE = os.path.join(VAULT_PATH, "intruder_log.txt")
BRIDGE_FILE = os.path.join(VAULT_PATH, "bridge_logs.txt")

if not os.path.exists(VAULT_PATH): os.makedirs(VAULT_PATH)

# Standort-Daten für Syke
HOME_BASE = {"City": "Syke", "lat": 52.9126, "lon": 8.8217}

class SilasGuardian:
    def __init__(self):
        # Initialisierung der System-Zustände
        if 'auth_level' not in st.session_state: st.session_state.auth_level = "A0"
        if 'login_time' not in st.session_state: st.session_state.login_time = None
        if 'scan_active' not in st.session_state: st.session_state.scan_active = False
        if 'vault_destroyed' not in st.session_state: st.session_state.vault_destroyed = False
        if 'crash' not in st.session_state: st.session_state.crash = False
        if 'blackout' not in st.session_state: st.session_state.blackout = False

    def write_log(self, filename, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(filename, "a") as f:
            f.write(f"[{timestamp}] {message}\n")

    def reset_system(self):
        # Kompletter System-Reset zurück auf A0
        st.session_state.auth_level = "A0"
        st.session_state.login_time = None
        st.session_state.scan_active = False
        st.session_state.vault_destroyed = False
        st.session_state.crash = False
        st.session_state.blackout = False
        st.rerun()

    def render(self):
        # --- CUSTOM CSS FÜR DEN TUFF-LOOK ---
        st.markdown("""
            <style>
            .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
            .stTabs [data-baseweb="tab-list"] { background-color: #050505; border-bottom: 1px solid #004400; }
            .stTabs [data-baseweb="tab"] { color: #00ff41 !important; }
            .terminal-box { background-color: #001100; border: 1px solid #00ff41; padding: 10px; border-radius: 5px; margin-bottom: 10px; }
            .stProgress > div > div > div > div { background-image: linear-gradient(to right, #004400, #00ff41); box-shadow: 0 0 10px #00ff41; }
            </style>
            """, unsafe_allow_html=True)

        # --- SICHERHEITS-FALLEN (BLACKOUT & CRASH) ---
        if st.session_state.blackout:
            st.markdown("<style>.main { background-color: #000 !important; cursor: none !important; }</style>", unsafe_allow_html=True)
            if st.button(" ", key="hidden_reset"): self.reset_system()
            return

        if st.session_state.crash:
            st.title("☣️ SYSTEM_HALTED")
            st.write("CRITICAL EXCEPTION IN SECTOR_0. PLEASE ENTER OVERRIDE CODE.")
            cols = st.columns(4)
            if cols[0].button("0x0B12"): self.write_log(LOG_FILE, "FAILED OVERRIDE: 0x0B12"); st.session_state.blackout = True; st.rerun()
            if cols[1].button("0xC991"): self.write_log(LOG_FILE, "FAILED OVERRIDE: 0xC991"); st.session_state.blackout = True; st.rerun()
            if cols[2].button("0xAF32"): self.reset_system() # Echter Code
            if cols[3].button("0x82FF"): self.write_log(LOG_FILE, "FAILED OVERRIDE: 0x82FF"); st.session_state.blackout = True; st.rerun()
            return

        # --- LOGIN-PHASE (A0) ---
        if st.session_state.auth_level == "A0":
            st.title("🛡️ SilasGuardian Login")
            ident = st.text_input("Ident (Masterkey)", type="password", key="l_id")
            pwd = st.text_input("Sektor-Passwort", type="password", key="l_pw")
            if st.button("Initialisiere Boot-Sequenz"):
                # Authentifizierung: Silas & Data
                if ident.lower() == "silas" and pwd.lower() == "data":
                    st.session_state.auth_level
