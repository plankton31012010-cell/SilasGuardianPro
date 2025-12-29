import streamlit as st
import time

# --- SYSTEM KONFIGURATION ---
st.set_page_config(
    page_title="SilasGuardian Pro", 
    page_icon="🛡️", 
    layout="wide", # Auf Wide gestellt für bessere Übersicht auf dem iPad
    initial_sidebar_state="expanded"
)

# Zugangsdaten
MASTER_KEY = "silas"
SEKTOR_PWS = {
    "Sektor 3: Zentral-Datenbank": "data",
    "Sektor 4: Netzwerk-Knoten": "strike",
    "Sektor 5: Firewall-Mainframe": "scan"
}

# --- SESSION STATE (Speichert den Login-Status) ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# --- LOGIN BEREICH ---
if not st.session_state.authenticated:
    st.title("🛡️ SilasGuardian Pro | Terminal Login")
    user_input = st.text_input("MASTER-KEY", type="password")
    if st.button("LOGIN"):
        if user_input == MASTER_KEY:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("ZUGRIFF VERWEIGERT")

# --- HAUPTSYSTEM ---
else:
    st.sidebar.title("🛡️ Kontrollzentrum")
    menu = st.sidebar.radio("Navigation", ["System-Status", "Sektor-Zugriff", "Sicherheits-Log", "Notfall-Lockdown"])

    if menu == "System-Status":
        # DIE NEUE WILLKOMMENS-NACHRICHT (Fest eingebaut)
        st.success(f"### ✅ Identität bestätigt: Willkommen zurück, Silas!")
        st.write(f"System-Zeit: {time.strftime('%H:%M:%S')} | Status: Gesichert")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Netzwerk", "ONLINE")
        col2.metric("Sektoren", "3 GEsichert")
        col3.metric("CPU", "12%")
        
        st.info("**Hinweis:** Alle Sektoren sind im Standby. Zugriff über das Menü links anfordern.")

    elif menu == "Sektor-Zugriff":
        st.title("Sektor-Kontrolle")
        sektor = st.selectbox("Sektor wählen", list(SEKTOR_PWS.keys()))
        pw = st.text_input(f"Passwort für {sektor}", type="password")
        
        if st.button("Zugriff anfordern"):
            if pw == SEKTOR_PWS[sektor]:
                st.success(f"🔓 ZUGRIFF GEWÄHRT - {sektor}")
                
                # INHALT FÜR SEKTOR 3
                if sektor == "Sektor 3: Zentral-Datenbank":
                    st.divider()
                    st.subheader("📁 GEHEIME ARCHIV-DATEN")
                    st.warning("Vertrauliche Informationen - Nur für Silas")
                    st.write("1. **Projekt 'Alpha Strike'**: Aktiv")
                    st.write("2. **Server-Standort**: Sektor 0 (Verschlüsselt)")
                    st.write("3. **Letztes Backup**: Heute " + time.strftime("%H:%M"))
                
                # INHALT FÜR SEKTOR 4
                elif sektor == "Sektor 4: Netzwerk-Knoten":
                    st.divider()
                    st.subheader("🌐 NETZWERK-ÜBERWACHUNG")
                    st.write("Führe aktiven Scan durch...")
                    st.progress(85)
                    st.code("SCANNING... IP 192.168.1.1 [CLEAN]\nSCANNING... IP 10.0.0.5 [CLEAN]")

            else:
                st.error("❌ PASSWORT FALSCH - ZUGRIFF VERWEIGERT")

    elif menu == "Sicherheits-Log":
        st.title("System-Protokoll")
        st.code(f"[{time.strftime('%H:%M:%S')}] User 'Silas' logged in.\n[STATUS] Sektor-Abfrage bereit.")

    elif menu == "Notfall-Lockdown":
        if st.button("🚨 SYSTEM-LOCKDOWN AUSLÖSEN"):
            st.session_state.authenticated = False
            st.rerun()

    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()
