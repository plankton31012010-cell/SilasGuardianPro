import streamlit as st
import time
import pandas as pd

# --- SYSTEM KONFIGURATION ---
st.set_page_config(
    page_title="SilasGuardian Pro | CORE v12.2", 
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

# --- ABSOLUTE SPERR-LOGIK ---
current_time = time.time()
if st.session_state.lockout_time > current_time:
    remaining = int(st.session_state.lockout_time - current_time)
    st.error(f"🚨 SYSTEM-LOCKDOWN: Zugriff gesperrt für {remaining}s.")
    time.sleep(1)
    st.rerun()
    st.stop()

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
    
    # .strip() verhindert Fehler durch Leerzeichen beim Master-Key
    user_input = st.text_input("Master-Key eingeben", type="password").strip()
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
                st.session_state.lockout_time = time.time() + 60
                st.rerun()
            else:
                st.error(f"ZUGRIFF VERWEIGERT! Noch {3 - st.session_state.failed_attempts} Versuche.")

# --- HAUPTSYSTEM ---
else:
    st.sidebar.title("🛡️ Core Control")
    menu = st.sidebar.radio("Sicherheits-Ebenen", ["Dashboard", "Sektor-Terminal", "Intrusion Logs"])

    if menu == "Dashboard":
        st.success("### ✅ System Online: Willkommen Silas")
        st.write(f"Status: **Scharfgeschaltet** | Verschlüsselung: **Aktiv**")
        st.info("Alle System-Zugriffe werden im IDS-Protokoll gespeichert.")

    elif menu == "Sektor-Terminal":
        st.subheader("Sektor-Verschlüsselung aufheben")
        sektor_wahl = st.selectbox("Sektor wählen", list(SEKTOR_PWS.keys()))
        
        # .strip() bereinigt die Eingabe von unsichtbaren Leerzeichen
        pw_input = st.text_input("Sektor-Passwort", type="password").strip()
        
        if st.button("Entschlüsseln"):
            # Vergleich der Eingabe mit dem hinterlegten Passwort
            if pw_input == SEKTOR_PWS[sektor_wahl]:
                st.success(f"🔓 Zugriff auf {sektor_wahl} gewährt.")
                
                # Flexible Abfrage über die Sektor-Nummer
                if "Sektor 3" in sektor_wahl:
                    st.divider()
                    st.subheader("📁 ARCHIV-DATEN")
                    st.write("- Projekt AlphaStrike: Dokumentation geladen.")
                    st.write("- Sicherheits-Status: Stabil.")
                
                elif "Sektor 4" in sektor_wahl:
                    st.divider()
                    st.subheader("🌐 NETZWERK-STATUS")
                    st.code("NODE-1: AKTIV\nNODE-2: AKTIV\nSCAN: LÄUFT...")
                    st.progress(100)
                
                elif "Sektor 5" in sektor_wahl:
                    st.divider()
                    st.subheader("🔥 FIREWALL-MONITOR")
                    st.error("Brute-Force-Detection: ONLINE")
                    st.write(f"Registrierte Fehlversuche: {st.session_state.failed_attempts}")
            else:
                st.error("🚨 PASSWORT INKORREKT")
                st.session_state.security_logs.append({"Zeit": time.strftime("%H:%M:%S"), "Ereignis": f"Sektor-Fehlzugriff: {sektor_wahl}", "Status": "CRITICAL"})

    elif menu == "Intrusion Logs":
        st.header("🕵️ System-Protokolle (IDS)")
        st.table(pd.DataFrame(st.session_state.security_logs))

    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()
