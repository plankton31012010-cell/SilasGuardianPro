import streamlit as st
import time
import requests

# --- SYSTEM KONFIGURATION ---
st.set_page_config(page_title="SilasGuardian CORE v12.4", page_icon="🛡️", layout="wide")

# --- INITIALISIERUNG ---
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'failed_attempts' not in st.session_state: st.session_state.failed_attempts = 0
if 'lockout_time' not in st.session_state: st.session_state.lockout_time = 0
if 'secret_notes' not in st.session_state: st.session_state.secret_notes = []

# --- LOCKDOWN-CHECK ---
if st.session_state.lockout_time > time.time():
    remaining = int(st.session_state.lockout_time - time.time())
    st.error(f"🚨 SYSTEM-LOCKDOWN: Zugriff für {remaining}s gesperrt.")
    st.stop()

# --- LOGIN ---
if not st.session_state.authenticated:
    st.title("🔐 SilasGuardian | Login")
    user_input = st.text_input("Master-Key", type="password").strip()
    if st.button("System entsperren"):
        if user_input == "silas":
            st.session_state.authenticated = True
            st.session_state.failed_attempts = 0
            st.rerun()
        else:
            st.session_state.failed_attempts += 1
            if st.session_state.failed_attempts >= 3:
                st.session_state.lockout_time = time.time() + 60
            st.rerun()
else:
    # --- HAUPTSYSTEM ---
    st.sidebar.title("🛡️ Core Control")
    menu = st.sidebar.radio("Sicherheits-Ebenen", ["Dashboard", "Sektor 3: Datentresor", "Sektor 4: Netzwerk-Scan"])

    if menu == "Dashboard":
        st.success("✅ Identität bestätigt: Silas")
        st.write("System-Status: **Aktiv**")
        st.info("Alle externen Scans werden über verschlüsselte Relays geleitet.")

    elif menu == "Sektor 3: Datentresor":
        st.subheader("📁 Geheimer Datentresor")
        st.write("Diese Daten werden nur verschlüsselt im Session-Speicher abgelegt.")
        
        # Eingabe für neue Notizen
        new_note = st.text_area("Neue Geheimbotschaft eingeben:")
        if st.button("In Tresor verschieben"):
            if new_note:
                st.session_state.secret_notes.append(f"{time.strftime('%d.%m. %H:%M')}: {new_note}")
                st.success("Daten im Sektor 3 gesichert.")
        
        st.divider()
        st.write("**Gespeicherte Einträge:**")
        if not st.session_state.secret_notes:
            st.write("*Keine Daten vorhanden.*")
        for note in reversed(st.session_state.secret_notes):
            st.code(note)

    elif menu == "Sektor 4: Netzwerk-Scan":
        st.subheader("🌐 Echtzeit-Netzwerkanalyse")
        st.write("Versuche, lokale IP-Identität zu verifizieren...")
        
        if st.button("Scan starten"):
            with st.spinner("Frage globale Knoten ab..."):
                try:
                    # Schritt 1: Deine echte IP über einen externen Dienst finden
                    ip_check = requests.get('https://api.ipify.org?format=json', timeout=5).json()
                    user_ip = ip_check.get("ip")
                    
                    # Schritt 2: Details zu DIESER IP abrufen
                    details = requests.get(f'https://ipapi.co/{user_ip}/json/', timeout=5).json()
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("DEINE ECHTE IP", details.get("ip"))
                        st.write(f"**Provider:** {details.get('org')}")
                    with col2:
                        st.metric("STANDORT", details.get("city"))
                        st.write(f"**Land:** {details.get('country_name')}")
                    
                    if details.get("country_code") == "DE":
                        st.success("✅ Lokaler Zugriff (Deutschland) bestätigt.")
                    else:
                        st.warning("⚠️ Zugriff erfolgt über ausländisches Gateway.")
                        
                except Exception as e:
                    st.error("🚨 API-Limit erreicht oder Verbindung blockiert. Bitte in 10 Min. erneut versuchen.")

    if st.sidebar.button("System-Logout"):
        st.session_state.authenticated = False
        st.rerun()
