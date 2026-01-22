import streamlit as st
import os
import time
import datetime
import pandas as pd

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

    def write_log(self, filename, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(filename, "a") as f:
            f.write(f"[{timestamp}] {message}\n")

    def render(self):
        # --- FUNKTION 5: CUSTOM CYBER-STYLES ---
        st.markdown("""
            <style>
            .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
            
            /* Custom Progress Bar */
            .stProgress > div > div > div > div {
                background-image: linear-gradient(to right, #004400, #00ff41);
                box-shadow: 0 0 15px #00ff41;
            }
            
            /* Terminal Look für Logs */
            .terminal-text {
                color: #00ff41;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                line-height: 1.2;
                background-color: #001100;
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #004400;
            }
            </style>
            """, unsafe_allow_html=True)

        # --- LOGIN-CHECK ---
        if st.session_state.auth_level == "A0":
            st.title("🛡️ SilasGuardian Login")
            ident = st.text_input("Ident", type="password", key="login_id")
            pwd = st.text_input("Passwort", type="password", key="login_pw")
            if st.button("Boot"):
                if ident.lower() == "silas" and pwd.lower() == "data":
                    st.session_state.auth_level = "A1+"
                    st.session_state.login_time = time.time()
                    st.rerun()
            return

        # --- DYNAMISCHE BEGRÜSSUNG (5s) ---
        elapsed = time.time() - st.session_state.login_time
        if elapsed < 5:
            st.title("Willkommen Anton")
            st.caption(f"Systemzugriff gewährt. Initialisiere Module... {5 - int(elapsed)}s")
            time.sleep(1); st.rerun()
        else:
            st.title("🛡️ SilasGuardian | Core-Terminal")

        tabs = st.tabs(["📡 Scanner", "📂 Sektor 3", "💬 Bridge", "🛡️ Sektor Zero"])

        # --- 1. SCANNER (UPGRADED VISUALS) ---
        with tabs[0]:
            st.subheader("📡 Deep-Net-Inspector v2.0")
            
            if st.button("Deep Scan starten", key="start_scan"):
                st.session_state.scan_active = False
                
                # Terminal Log Animation
                log_placeholder = st.empty()
                progress_bar = st.progress(0)
                
                tech_logs = [
                    "INITIALIZING SYN SCAN...", "REACHING GATEWAY 192.168.1.1...",
                    "BYPASSING LOCAL FIREWALL...", "COLLECTING MAC ADDRESSES...",
                    "DECRYPTING DEVICE SIGNATURES...", "MAPPING NETWORK NODES...",
                    "COMPILING DATA TABLES...", "SCAN COMPLETE."
                ]
                
                for i in range(100):
                    time.sleep(0.03)
                    progress_bar.progress(i + 1)
                    
                    # Logik: Zeige alle paar Prozent eine neue technische Zeile
                    current_log_idx = min(i // 15, len(tech_logs) - 1)
                    log_placeholder.markdown(f"""
                        <div class="terminal-text">
                        > {tech_logs[current_log_idx]}<br>
                        > ADDR_PTR: 0x{random.randint(1000, 9999)}<br>
                        > PACKET_STREAMS: {i*124} KB/s
                        </div>
                    """, unsafe_allow_html=True)
                
                st.session_state.scan_active = True
                st.success("✅ Netzwerk-Analyse abgeschlossen.")

            if st.session_state.get('scan_active'):
                st.divider()
                scan_data = [
                    {"IP": "192.168.1.1", "Gerät": "FritzBox 7590", "MAC": "00:E0:4C:53:12:01", "Info": "Gateway"},
                    {"IP": "192.168.1.42", "Gerät": "Apple iPhone 15", "MAC": "7C:D1:C3:94:02:88", "Info": "Mobil"},
                    {"IP": "192.168.1.105", "Gerät": "Sony PS5", "MAC": "44:F4:11:00:AA:BB", "Info": "Konsole"}
                ]
                st.table(pd.DataFrame(scan_data))

        # --- 2. SEKTOR 3 (VAULT) ---
        with tabs[1]:
            st.subheader("📂 Sektor 3 - Vault")
            if st.checkbox("Logs einsehen"):
                if os.path.exists(LOG_FILE):
                    with open(LOG_FILE, "r") as f: st.text_area("Intruder Logs", f.read(), height=150)
                if os.path.exists(BRIDGE_FILE):
                    with open(BRIDGE_FILE, "r") as f: st.text_area("Bridge Archiv", f.read(), height=150)
            st.divider()
            up = st.file_uploader("Datei hochladen")
            if up:
                with open(os.path.join(VAULT_PATH, up.name), "wb") as f: f.write(up.getbuffer())
            for f_name in os.listdir(VAULT_PATH):
                if f_name not in ["intruder_log.txt", "bridge_logs.txt"]:
                    with open(os.path.join(VAULT_PATH, f_name), "rb") as fb:
                        st.download_button(f"🔓 {f_name} öffnen", fb, file_name=f_name, key=f_name)

        # --- 3. BRIDGE ---
        with tabs[2]:
            st.subheader("💬 Comms-Bridge")
            new_msg = st.text_input("Nachricht...", key="msg_input")
            if st.button("Senden"):
                if new_msg:
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    with open(BRIDGE_FILE, "a") as f:
                        f.write(f"[{timestamp}] Anton: {new_msg}\n")
                    st.rerun()
            if os.path.exists(BRIDGE_FILE):
                with open(BRIDGE_FILE, "r") as f:
                    for line in reversed(f.readlines()): st.code(line.strip())

        # --- 4. SEKTOR ZERO ---
        with tabs[3]:
            if st.toggle("PANIC MODE"): 
                st.session_state.crash = True
                st.rerun()
            if st.button("🚨 Shutdown"): 
                st.session_state.auth_level = "A0"
                st.rerun()

if __name__ == "__main__":
    import random
    SilasGuardian().render()
