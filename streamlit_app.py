import streamlit as st
import os
import time
import datetime
import pandas as pd
import random

# Versuche Plotly zu laden, falls es fehlt, gibt es eine Warnung statt eines Absturzes
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

# Standort-Daten für Syke
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
        st.session_state.auth_level = "A0"
        st.session_state.login_time = None
        st.session_state.scan_active = False
        st.session_state.vault_destroyed = False
        st.session_state.crash = False
        st.session_state.blackout = False
        st.rerun()

    def render(self):
        # --- CSS ---
        st.markdown("""
            <style>
            .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
            .stTabs [data-baseweb="tab-list"] { background-color: #050505; }
            .stTabs [data-baseweb="tab"] { color: #00ff41 !important; }
            .terminal-box { background-color: #001100; border: 1px solid #00ff41; padding: 10px; border-radius: 5px; margin-bottom: 10px; font-size: 12px; }
            </style>
            """, unsafe_allow_html=True)

        # --- SICHERHEITSEBENEN ---
        if st.session_state.blackout:
            st.markdown("<style>.main { background-color: #000 !important; }</style>", unsafe_allow_html=True)
            if st.button(" ", key="hidden_reset"): self.reset_system()
            return

        if st.session_state.crash:
            st.title("☣️ SYSTEM_HALTED")
            cols = st.columns(4)
            if cols[0].button("0x0B12"): self.write_log(LOG_FILE, "Falle: 0x0B12"); st.session_state.blackout = True; st.rerun()
            if cols[1].button("0xC991"): self.write_log(LOG_FILE, "Falle: 0xC991"); st.session_state.blackout = True; st.rerun()
            if cols[2].button("0xAF32"): self.reset_system()
            if cols[3].button("0x82FF"): self.write_log(LOG_FILE, "Falle: 0x82FF"); st.session_state.blackout = True; st.rerun()
            return

        # --- LOGIN ---
        if st.session_state.auth_level == "A0":
            st.title("🛡️ SilasGuardian Login")
            ident = st.text_input("Ident", type="password", key="l_id")
            pwd = st.text_input("Sektor-Passwort", type="password", key="l_pw")
            if st.button("Boot"):
                if ident.lower() == "silas" and pwd.lower() == "data":
                    st.session_state.auth_level = "A1+"
                    st.session_state.login_time = time.time()
                    st.rerun()
                else:
                    st.error("ZUGRIFF VERWEIGERT.")
            return

        # --- TIMER ---
        elapsed = time.time() - st.session_state.login_time
        if elapsed < 5:
            st.title("Willkommen Anton")
            st.caption(f"Lade System-Kern... {5 - int(elapsed)}s")
            time.sleep(1); st.rerun()

        # --- DASHBOARD ---
        tabs = st.tabs(["🌍 Threat-Map", "📡 Scanner", "📂 Sektor 3", "💬 Bridge", "🛡️ Sektor Zero"])

        with tabs[0]: # Weltkarte
            if PLOTLY_AVAILABLE:
                attacks = []
                for _ in range(7):
                    attacks.append({'lat': random.uniform(-30, 60), 'lon': random.uniform(-100, 120), 'Type': 'Threat', 'Color': 'Red'})
                attacks.append({'lat': HOME_BASE['lat'], 'lon': HOME_BASE['lon'], 'Type': 'HOME BASE (Syke)', 'Color': 'Blue'})
                df_map = pd.DataFrame(attacks)
                fig = px.scatter_geo(df_map, lat='lat', lon='lon', hover_name='Type', color='Color',
                                     color_discrete_map={'Red': '#ff0000', 'Blue': '#008cff'},
                                     projection="natural earth")
                fig.update_layout(template="plotly_dark", margin=dict(l=0, r=0, t=0, b=0), showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("Weltkarten-Modul lädt noch... Bitte 'requirements.txt' prüfen.")

        with tabs[1]: # Scanner
            if st.button("Deep Scan starten"):
                st.session_state.scan_active = False
                p = st.progress(0)
                l = st.empty()
                for i in range(100):
                    time.sleep(0.01)
                    p.progress(i + 1)
                    l.markdown(f"<div class='terminal-box'>> ANALYZING... {i+1}%</div>", unsafe_allow_html=True)
                st.session_state.scan_active = True
                st.rerun()
            if st.session_state.get('scan_active'):
                st.table(pd.DataFrame([{"IP": "192.168.1.1", "Device": "Gateway (FritzBox)"}]))

        with tabs[2]: # Vault
            if st.session_state.vault_destroyed:
                st.error("VAULT EMPTY")
                if st.button("Restore"): st.session_state.vault_destroyed = False; st.rerun()
            else:
                if st.button("🧨 SELBSTZERSTÖRUNG"): st.session_state.vault_destroyed = True; st.rerun()
                st.divider()
                for f_name in os.listdir(VAULT_PATH):
                    if f_name not in ["intruder_log.txt", "bridge_logs.txt"]:
                        with open(os.path.join(VAULT_PATH, f_name), "rb") as fb:
                            st.download_button(f"🔓 {f_name}", fb, file_name=f_name, key=f_name)

        with tabs[3]: # Bridge
            m = st.text_input("Message...")
            if st.button("Send"):
                self.write_log(BRIDGE_FILE, f"Anton: {m}")
                st.rerun()
            if os.path.exists(BRIDGE_FILE):
                with open(BRIDGE_FILE, "r") as f:
                    for line in reversed(f.readlines()): st.code(line.strip())

        with tabs[4]: # Zero
            if st.toggle("PANIC MODE"): st.session_state.crash = True; st.rerun()
            if st.button("🚨 Shutdown"): self.reset_system()

if __name__ == "__main__":
    SilasGuardian().render()
