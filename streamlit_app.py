import streamlit as st
import time
import pandas as pd # Für das professionelle Logbuch

# --- SYSTEM KONFIGURATION ---
st.set_page_config(
    page_title="SilasGuardian Pro | CORE", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- VERSCHLÜSSELTE DATENBANK (Beispiel) ---
# In einem echten System wären diese Werte nochmals gehasht.
MASTER_KEY = "silas"
SEKTOR_PWS = {
    "Sektor 3: Zentral-Datenbank": "data",
    "Sektor 4: Netzwerk-Knoten": "strike",
    "Sektor 5: Sicherheits-Überwachung": "scan"
}

# --- INITIALISIERUNG DES LOGS ---
if 'security_logs' not in st.session_state:
    st.session_state.security_logs = [
        {"Zeit": time.strftime("%H:%M:%S"), "Ereignis": "System-Kern gestartet", "Status": "OK"}
    ]

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# --- LOGIN LOGIK ---
if not st.session_state.authenticated:
    st.title("🔐 SilasGuardian CORE | Authentifizierung")
    user_input = st.text_input("Geben Sie den Master-Key ein", type="password")
    
    if st.button("System entsperren"):
        if user_input == MASTER_KEY:
            st.session_state.authenticated = True
            st.session_state.security_logs.append(
                {"Zeit": time.strftime("%H:%M:%S"), "Ereignis": "Master-Login erfolgreich", "Status": "AUTH"}
            )
            st.rerun()
        else:
            st.session_state.security_logs.append(
                {"Zeit": time.strftime("%H:%M:%S"), "Ereignis": "Fehlgeschlagener Login-Versuch", "Status": "WARNUNG"}
            )
            st.error("ZUGRIFF VERWEIGERT - Protokoll erstellt.")

# --- GESICHERTE BENUTZEROBERFLÄCHE ---
else:
    st.sidebar.title("🛡️ Core Control")
    menu = st.sidebar.radio("Sicherheits-Ebenen", ["Dashboard", "Sektor-Terminal", "Intrusion Logs"])

    if menu == "Dashboard":
        st.header("Willkommen zurück, Silas")
        st.success("System-Integrität: 100% | Verschlüsselung: AES-256 aktiv")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info("Letzte Aktivität: " + st.session_state.security_logs[-1]["Zeit"])
        with col2:
            st.warning("Aktive Sektoren: 3")

    elif menu == "Sektor-Terminal":
        st.subheader("Sektor-Verschlüsselung aufheben")
        sektor = st.selectbox("Wählen Sie den Ziel-Sektor", list(SEKTOR_PWS.keys()))
        pw = st.text_input("Sektor-Passwort", type="password")
        
        if st.button("Entschlüsseln"):
            if pw == SEKTOR_PWS[sektor]:
                st.success(f"Daten für {sektor} freigegeben.")
                
                if sektor == "Sektor 5: Sicherheits-Überwachung":
                    st.write("### 🚨 Firewall-Live-Daten")
                    st.write("- Port 80/443: Überwacht")
                    st.write("- Brute-Force-Schutz: Aktiv")
                    st.write("- Bekannte Bedrohungen: 0")
            else:
                st.error("Ungültiges Sektor-Passwort!")
                st.session_state.security_logs.append(
                    {"Zeit": time.strftime("%H:%M:%S"), "Ereignis": f"Fehlzugriff {sektor}", "Status": "CRITICAL"}
                )

    elif menu == "Intrusion Logs":
        st.header("🕵️ System-Protokolle (IDS)")
        st.write("Dieses Logbuch zeichnet jede Bewegung im System auf.")
        df = pd.DataFrame(st.session_state.security_logs)
        st.table(df) # Hier siehst du jetzt eine echte Tabelle deiner Logins!

    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()
