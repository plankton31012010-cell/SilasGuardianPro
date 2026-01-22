import streamlit as st
import os
import time
import datetime
import pandas as pd
import random
import plotly.express as px # Für die Weltkarte

# --- SYSTEM-SETUP ---
st.set_page_config(page_title="SilasGuardian", page_icon="🛡️", layout="wide")
VAULT_PATH = "sector_3_vault"
LOG_FILE = os.path.join(VAULT_PATH, "intruder_log.txt")
BRIDGE_FILE = os.path.join(VAULT_PATH, "bridge_logs.txt")
if not os.path.exists(VAULT_PATH): os.makedirs(VAULT_PATH)

class SilasGuardian:
    def __init__(self):
        if 'auth_level' not in st.session_state: st.session_state.auth_level = "A0"
        if 'login_time' not in st.session_state: st.session_state.login_time = None
        if 'scan_active' not in st.session_state: st.session_state.scan_active = False

    def render(self):
        st.markdown("""
            <style>
            .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
            .stTabs [data-baseweb="tab-list"] { background-color: #050505; }
            .stTabs [data-baseweb="tab"] { color: #00ff41 !important; }
            </style>
            """, unsafe_allow_html=True)

        if st.session_state.auth_level == "A0":
            st.title("🛡️ SilasGuardian Login")
            ident = st.text_input("Ident", type="password")
            pwd = st.text_input("Sektor-Passwort", type="password")
            if st.button("Boot"):
                if ident.lower() == "silas" and pwd.lower() == "data":
                    st.session_state.auth_level = "A1+"
                    st.session_state.login_time = time.time()
                    st.rerun()
            return

        elapsed = time.time() - st.session_state.login_time
        if elapsed < 5:
            st.title("Willkommen Anton")
            st.caption(f"Initialisiere Weltkarte... {5 - int(elapsed)}s")
            time.sleep(1); st.rerun()

        tabs = st.tabs(["🌍 Global Map", "📡 Scanner", "📂 Sektor 3", "💬 Bridge", "🛡️ Sektor Zero"])

        # --- 1. WELTKARTE (NEU) ---
        with tabs[0]:
            st.subheader("🌍 Real-Time Threat Map")
            # Zufällige Angriffsdaten generieren
            df = pd.DataFrame({
                'lat': [random.uniform(-50, 70) for _ in range(5)],
                'lon': [random.uniform(-120, 140) for _ in range(5)],
                'Angriffstyp': ['Brute Force', 'SQL Injection', 'DDoS', 'Malware', 'Phishing'],
                'Stärke': [random.randint(10, 100) for _ in range(5)]
            })
            fig = px.scatter_geo(df, lat='lat', lon='lon', hover_name='Angriffstyp', 
                                 size='Stärke', projection="natural earth",
                                 color_discrete_sequence=["#00ff41"])
            fig.update_layout(template="plotly_dark", margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig, use_container_width=True)

        # --- 2. SCANNER (STABIL) ---
        with tabs[1]:
            if st.button("Deep Scan starten"):
                st.session_state.scan_active = True
                pb = st.progress(0)
                for i in range(100): time.sleep(0.01); pb.progress(i + 1)
            if st.session_state.get('scan_active'):
                st.success("✅ Scan abgeschlossen.")
                st.table(pd.DataFrame([{"IP": "192.168.1.1", "Gerät": "FritzBox", "Status": "Aktiv"}]))

        # --- 3. SEKTOR 3 (MIT SELBSTZERSTÖRUNG) ---
        with tabs[2]:
            st.subheader("📂 Sektor 3 - Vault")
            if st.button("🧨 SELBSTZERSTÖRUNG AKTIVIEREN", type="primary"):
                with st.warning("Dateien werden unwiderruflich gelöscht..."):
                    for f in os.listdir(VAULT_PATH): os.remove(os.path.join(VAULT_PATH, f))
                    time.sleep(2)
                    st.error("Vault gesäubert. Alle Daten vernichtet.")
            st.divider()
            for f_name in os.listdir(VAULT_PATH):
                with open(os.path.join(VAULT_PATH, f_name), "rb") as fb:
                    st.download_button(f"🔓 {f_name}", fb, file_name=f_name, key=f_name)

        # --- RESTLICHE TABS ---
        with tabs[3]: # Bridge
            new_msg = st.text_input("Nachricht...")
            if st.button("Senden"):
                with open(BRIDGE_FILE, "a") as f: f.write(f"[{datetime.datetime.now().strftime('%H:%M')}] Anton: {new_msg}\n")
                st.rerun()
            if os.path.exists(BRIDGE_FILE):
                with open(BRIDGE_FILE, "r") as f:
                    for line in reversed(f.readlines()): st.code(line.strip())

        with tabs[4]: # Zero
            if st.toggle("PANIC MODE"): 
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open(LOG_FILE, "a") as f: f.write(f"[{timestamp}] ALARM: Panic Mode manuell aktiviert.\n")
                st.session_state.crash = True; st.rerun()
            if st.button("🚨 Shutdown"): st.session_state.auth_level = "A0"; st.rerun()

if __name__ == "__main__":
    SilasGuardian().render()
