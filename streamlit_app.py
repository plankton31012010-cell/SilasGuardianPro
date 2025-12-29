import streamlit as st
import time
import pandas as pd

# --- SYSTEM KONFIGURATION ---
st.set_page_config(
    page_title="SilasGuardian Pro | CORE v12.1", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SESSION STATE INITIALISIERUNG ---
if 'security_logs' not in st.session_state:
    st.session_state.security_logs = [{"Zeit": time.strftime("%H:%M:%S"), "Ereignis": "Kern-Initialisierung", "Status": "OK"}]
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'failed_attempts' not in st.session_state:
    st.session_state.failed_attempts = 0
if 'lockout_time' not in st.session_state:
    st.session_state.lockout_time = 0

# --- ABSOLUTE SPERR-LOGIK (Muss vor dem UI stehen) ---
current_time = time.time()
if st.session_state.lockout_time > current_time:
    remaining = int(st.session_state.lockout_time - current_time)
    st.error(f"🚨 SYSTEM-LOCKDOWN: Brute-Force Schutz aktiv. Zugriff gesperrt für {remaining}s.")
    time.sleep(1)
    st.rerun()
    st.stop() # Verhindert das Laden der restlichen App

# --- DATENBANK ---
MASTER_KEY = "silas"
SEKTOR_PWS = {
    "Sektor 3: Zentral-Datenbank": "data",
    "Sektor 4: Netzwerk-Knoten": "strike",
    "Sektor 5: Sicherheits-Überwachung": "scan"
}

# --- LOGIN BEREICH ---
if not st.session_state.authenticated:
    st.title("🔐 SilasGuardian CORE | Login")
    
    user_input = st.text_input("Master-Key eingeben", type="password")
    if st.button("System entsperren"):
        if user_input == MASTER_KEY:
            st.session_state.authenticated = True
            st.session_state.failed_attempts = 0
            st.session_state.security_logs.append({"Zeit": time.strftime("%H:%M:%S"), "Ereignis": "Master-Login", "Status": "AUTH"})
            st.rerun()
        else:
            st.session_state.failed_attempts += 1
            st.session_state.security_logs.append({"Zeit": time.strftime("%H:%M:%S"), "Ereignis": f"Fehl-Login (Versuch {st.session_state.failed_attempts})", "Status": "WARNUNG"})
            
            if st.session_state.failed_attempts >= 3:
                st.session_state.lockout_time = time.time() + 60 # 60 Sekunden Sperre
                st.rerun()
            else:
                st.error(f"ZUGRIFF VERWEIGERT! Noch {3 - st.session_state.failed_attempts} Versuche bis zum Lockdown.")

# --- HAUPTSYSTEM ---
else:
    st.sidebar.title("🛡️ Core Control")
    menu = st.sidebar.radio("Sicherheits-Ebenen", ["Dashboard", "Sektor-Terminal", "Intrusion Logs"])

    if menu == "Dashboard":
        st.success("### ✅ System Online: Willkommen Silas")
        st.write(f"Verschlüsselungsebene: **AES-256** | Status: **Scharf**")
        st.info("Alle Versuche werden im Intrusion-Log protokolliert.")

    elif menu == "Sektor-Terminal":
        st.subheader("Sektor-Verschlüsselung")
        sektor = st.selectbox("Sektor wählen", list(SEKTOR_PWS.keys()))
        pw = st.text_input("Passwort", type="password")
        
        if st.button("Entschlüsseln"):
            if pw == SEKTOR_PWS[sektor]:
                st.success(f"🔓 {sektor} geöffnet")
                
                if sektor == "Sektor 3: Zentral-Datenbank":
                    st.divider()
                    st.subheader("📁 ARCHIV-DATEN")
                    st.write("- **Projekt AlphaStrike:** Dokumentation v1.0 geladen.")
                    st.write("- **Sektor 0:** Status versteckt.")
                
                elif sektor == "Sektor 4: Netzwerk-Knoten":
                    st.divider()
                    st.subheader("🌐 NETZWERK-ÜBERWACHUNG")
                    st.code("NODE-1: AKTIV\nNODE-2: AKTIV")
                
                elif sektor == "Sektor 5: Sicherheits-Überwachung":
                    st.divider()
                    st.subheader("🔥 FIREWALL-STATUS")
                    st.error("Brute-Force-Detection: ONLINE")
                    st.write(f"Fehlversuche im Speicher: {st.session_state.failed_attempts}")
            else:
                st.error("Sektor-Passwort falsch!")

    elif menu == "Intrusion Logs":
        st.header("🕵️ System-Protokolle (IDS)")
        st.table(pd.DataFrame(st.session_state.security_logs))

    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()
