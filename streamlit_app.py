import streamlit as st
import os
import time
import datetime
import pandas as pd
import random

# Versuche Plotly zu laden für die Weltkarte
try:
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# --- SYSTEM-SETUP ---
VAULT_PATH = "sector_3_vault"
LOG_FILE = os.path.join(VAULT_PATH, "intruder_log.txt")
BRIDGE_FILE = os.path.join(VAULT_PATH, "bridge_logs.txt")

if not os.path.exists(VAULT_PATH): 
    os.makedirs(VAULT_PATH)

# Dein Standort: Syke, Deutschland
HOME_BASE = {"City": "Syke", "lat": 52.9126, "lon": 8.8217}

class SilasGuardian:
    def __init__(self):
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
        st.session_state.update({
            "auth_level": "A0", "login_time": None, "scan_active": False,
            "vault_destroyed": False, "crash": False, "blackout": False
        })
        st.rerun()

    def render(self):
        # --- CSS FÜR DEN CYBER-LOOK ---
        st.markdown("""
            <style>
            .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
            .stTabs [data-baseweb="tab-list"] { background-color: #050505; border-bottom: 1px solid #004400; }
            .stTabs [data-baseweb="tab"] { color: #00ff41 !important; }
            .terminal-box { background-color: #001100; border: 1px solid #00ff41; padding: 10px; border-radius: 5px; font-size: 12px; }
            .stProgress > div > div > div > div { background-image: linear-gradient(to right, #004400, #00ff41); box-shadow: 0 0 10px #00ff41; }
            </style>
            """, unsafe_allow_html=True)

        # --- SICHERHEITS-LOGIK ---
        if st.session_state.blackout:
            st.markdown("<style>.main { background-color: #000 !important; }</style>", unsafe_allow_html=True)
            if st.button(" ", key="hidden_reset"): self.reset_system()
            return

        if st.session_state.crash:
            st.title("☣️ SYSTEM_HALTED")
            cols = st.columns(4)
            if cols[0].button("0x0B12"): self.write_log(LOG_FILE, "ALARM 0x0B12"); st.session_state.blackout = True; st.rerun()
            if cols[1].button("0xC991"): self.write_log(LOG_FILE, "ALARM 0xC991"); st.session_state.blackout = True; st.rerun()
            if cols[2].button("0xAF32"): self.reset_system()
            if cols[3].button("0x82FF"): self.write_log(LOG_FILE, "ALARM 0x82FF"); st.session_state.blackout = True; st.rerun()
            return

        # --- LOGIN (A0) ---
        if st.session_state.auth_level == "A0":
            st.title("🛡️ SilasGuardian Login")
            ident = st.text_input("Ident", type="password", key="l_id")
            pwd = st.text_input("Sektor-Passwort", type="password", key="l_pw")
            if st.button("Boot-Sequenz starten"):
                if ident.lower() == "silas" and pwd.lower() == "data":
                    st.session_state.auth_level = "A1+"
                    st.session_state.login_time = time.time()
                    st.rerun()
                else:
                    st.error("ZUGRIFF VERWEIGERT.")
            return

        # --- INITIALISIERUNG ---
        elapsed = time.time() - st.session_state.login_time
        if elapsed < 5:
            st.title("Willkommen Anton")
            st.caption(f"Dechiffriere Sektoren... {5 - int(elapsed)}s")
            time.sleep(1); st.rerun()

        # --- TABS ---
        tabs = st.tabs(["🌍 Threat-Map", "📡 Scanner", "📂 Sektor 3", "💬 Bridge", "🛡️ Sektor Zero"])

        # 1. WELTKARTE (GRÜNE ANGRIFFE, ROTE HOMEBASE)
        with tabs[0]:
            if PLOTLY_AVAILABLE:
                st.subheader("🌍 Live-Überwachung: Globale Bedrohungen")
                threats = []
                # Zufällige Angriffe (Grün)
                for _ in range(12):
                    threats.append({
                        'lat': random.uniform(-35, 65), 'lon': random.uniform(-110, 140),
                        'Info': f"IP: {random.randint(1,255)}.{random.randint(1,255)}.x.x",
                        'Typ': random.choice(['Brute Force', 'DDoS', 'Port Scan']),
                        'Größe': random.randint(10, 40), 'Farbe': 'Grün'
                    })
                # Dein Heimatpunkt (Rot)
                threats.append({
                    'lat': HOME_BASE['lat'], 'lon': HOME_BASE['lon'],
                    'Info': 'HOME BASE (Syke)', 'Typ': 'CORE_PROTECTION',
                    'Größe': 50, 'Farbe': 'Rot'
                })
                
                df_map = pd.DataFrame(threats)
                fig = px.scatter_geo(df_map, lat='lat', lon='lon', size='Größe',
                                     hover_name='Info', hover_data={'Typ': True, 'Größe': False, 'lat': False, 'lon': False},
                                     color='Farbe', color_discrete_map={'Grün': '#00ff41', 'Rot': '#
