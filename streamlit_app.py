import streamlit as st
import time
import pandas as pd

# --- SYSTEM KONFIGURATION ---
st.set_page_config(
    page_title="SilasGuardian Pro | CORE v12", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- DATENBANK ---
MASTER_KEY = "silas"
SEKTOR_PWS = {
    "Sektor 3: Zentral-Datenbank": "data",
    "Sektor 4: Netzwerk-Knoten": "strike",
    "Sektor 5: Sicherheits-Überwachung": "scan"
}

# --- SESSION STATE INITIALISIERUNG ---
if 'security_logs' not in st.session_state:
    st.session_state.security_logs = [{"Zeit": time.strftime("%H:%M:%S"), "Ereignis": "Kern-Initialisierung", "Status": "OK"}]
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'failed_attempts' not in st.session_state:
    st.session_state.failed_attempts = 0
if 'lockout_time' not in st.session_state:
    st.session_state.lockout_time = 0

# --- BRUTE FORCE LOGIK ---
current_time = time.time()
is_locked = current_time < st.session_state.lockout_time

# --- LOGIN BEREICH ---
if not st.session_state.authenticated:
    st.title("🔐 SilasGuardian CORE | Login")
    
    if is_locked:
        remaining = int(st.session_state.lockout_time - current_time)
        st.error(f"⚠️ SYSTEM GESPERRT: Brute-Force erkannt. Versuchen Sie es in {remaining}s erneut.")
        time.sleep(1)
        st.rerun()
    else:
        user_input = st.text_input("Master-Key", type="password")
        if st.button("System entsperren"):
            if user_input == MASTER_KEY:
                st.session_state.authenticated = True
                st.session_state.failed_attempts = 0
                st.session_state.security_logs.append({"Zeit": time.strftime("%H:%M:%S"), "Ereignis": "Master-Login", "Status": "AUTH"})
                st.rerun()
            else:
                st.session_state.failed_attempts += 1
                st.session_state.security_logs.append({"Zeit": time.strftime("%H:%M:%S"), "Ereignis": "Fehl-Login", "Status": "WARNUNG"})
                if st.session_state.failed_attempts >= 3:
                    st.session_state.lockout_time = time.time() + 60 # 60 Sekunden Sperre
                    st.error("Zuviele Fehlversuche! System wird gesperrt.")
                else:
                    st.error(f"Zugriff verweigert! Versuch {st.session_state.failed_attempts}/3")

# --- HAUPTSYSTEM ---
else:
    st.sidebar.title("🛡️ Core Control")
    menu = st.sidebar.radio("Sicherheits-Ebenen", ["Dashboard", "Sektor-Terminal", "Intrusion Logs"])

    if menu == "Dashboard":
        st.success("### ✅ Zugriff gewährt: Willkommen Silas")
        st.info(f"System-Integrität: Gesichert | Letzter Login: {time.strftime('%H:%M')}")
        st.metric("Sicherheits-Level", "High", delta="Stable")

    elif menu == "Sektor-Terminal":
        st.subheader("Sektor-Verschlüsselung aufheben")
        sektor = st.selectbox("Sektor wählen", list(SEKTOR_PWS.keys()))
        pw = st.text_input("Sektor-Passwort", type="password")
        
        if st.button("Entschlüsseln"):
            if pw == SEKTOR_PWS[sektor]:
                st.success(f"🔓 {sektor} geöffnet")
                
                if sektor == "Sektor 3: Zentral-Datenbank":
                    st.divider()
                    st.subheader("📁 ARCHIV-DATEN")
                    st.write("- **Projekt AlphaStrike:** Testphase abgeschlossen.")
                    st.write("- **Masterkey-Status:** Unverändert.")
                
                elif sektor == "Sektor 4: Netzwerk-Knoten":
                    st.divider()
                    st.subheader("🌐 NETZWERK-ÜBERWACHUNG")
                    st.code("NODE-1: AKTIV\nNODE-2: AKTIV\nFIREWALL: FILTERND")
                    st.progress(100)
                
                elif sektor == "Sektor 5: Sicherheits-Überwachung":
                    st.divider()
                    st.subheader("🔥 FIREWALL-STATUS")
                    st.error("IDS-System: Scharfgeschaltet")
                    st.write("Versuche bis Sperre: 3")
            else:
                st.error("Falsches Passwort!")

    elif menu == "Intrusion Logs":
        st.header("🕵️ System-Protokolle (IDS)")
        st.table(pd.DataFrame(st.session_state.security_logs))

    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()
