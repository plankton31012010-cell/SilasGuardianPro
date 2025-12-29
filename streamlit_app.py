import streamlit as st
import time

# --- SYSTEM KONFIGURATION ---
st.set_page_config(page_title="SilasGuardian Pro", page_icon="🛡️", layout="centered", initial_sidebar_state="expanded")
# Zugangsdaten
MASTER_KEY = "silas"
SEKTOR_PWS = {
    "Sektor 3: Zentral-Datenbank": "data",
    "Sektor 4: Netzwerk-Knoten": "strike",
    "Sektor 5: Firewall-Mainframe": "scan"
}

# --- SESSION STATE (Speichert den Login) ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# --- LOGIN BEREICH ---
if not st.session_state.authenticated:
    st.title("🛡️ SilasGuardian Pro | Terminal Login")
    st.write("Autorisierung erforderlich für Firmen-Netzwerkzugriff.")
    
    user_input = st.text_input("MASTER-KEY", type="password")
    if st.button("LOGIN"):
        if user_input == MASTER_KEY:
            st.session_state.authenticated = True
            st.success("Identität bestätigt. Initialisiere...")
            time.sleep(1)
            st.rerun()
        else:
            st.error("ZUGRIFF VERWEIGERT: Ungültiger Key.")

# --- HAUPTSYSTEM ---
else:
    st.sidebar.title("🛡️ Kontrollzentrum")
    menu = st.sidebar.radio("Navigation", ["System-Status", "Sektor-Zugriff", "Sicherheits-Log", "Notfall-Lockdown"])

    if menu == "System-Status":
        st.title("System-Integrität: OK")
        c1, c2, c3 = st.columns(3)
        c1.metric("Knoten", "Aktiv")
        c2.metric("Bedrohung", "Null")
        c3.metric("Verschlüsselung", "AES-256")
        st.write("---")
        st.subheader("Echtzeit-Überwachung")
        st.info("Alle Systeme laufen im grünen Bereich.")

    elif menu == "Sektor-Zugriff":
        st.title("Sektor-Kontrolle")
        sektor = st.selectbox("Sektor wählen", list(SEKTOR_PWS.keys()))
        pw = st.text_input(f"Passwort für {sektor}", type="password")
        if st.button("Zugriff anfordern"):
            if pw == SEKTOR_PWS[sektor]:
                st.success(f"Zugriff auf {sektor} aktiv.")
            else:
                st.error("Ungültiges Sektor-Passwort!")

    elif menu == "Sicherheits-Log":
        st.title("System-Protokoll")
        st.code(f"[{time.strftime('%H:%M:%S')}] Firewall Integritäts-Check: OK\n[STATUS] System verschlüsselt.\n[USER] Master-Login Silas.")

    elif menu == "Notfall-Lockdown":
        st.title("⚠️ EMERGENCY OVERRIDE")
        if st.button("SOFORTIGER LOCKDOWN"):
            st.session_state.authenticated = False
            st.rerun()
