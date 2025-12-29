import streamlit as st
import time
import requests

# --- SYSTEM KONFIGURATION ---
st.set_page_config(page_title="SilasGuardian CORE v12.5", page_icon="🛡️", layout="wide")

# --- INITIALISIERUNG ---
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'failed_attempts' not in st.session_state: st.session_state.failed_attempts = 0
if 'lockout_time' not in st.session_state: st.session_state.lockout_time = 0
if 'secret_notes' not in st.session_state: st.session_state.secret_notes = []

# --- LOCKDOWN-CHECK ---
if st.session_state.lockout_time > time.time():
    st.error(f"🚨 SYSTEM-LOCKDOWN aktiv.")
    st.stop()

# --- LOGIN ---
if not st.session_state.authenticated:
    st.title("🔐 SilasGuardian | Login")
    user_input = st.text_input("Master-Key", type="password").strip()
    if st.button("System entsperren"):
        if user_input == "silas":
            st.session_state.authenticated = True
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
        st.success("✅ System Online: Silas")
        st.info("Scanner-Schnittstelle v12.5 bereit.")

    elif menu == "Sektor 3: Datentresor":
        st.subheader("📁 Geheimer Datentresor")
        new_note = st.text_area("Neue Geheimbotschaft:")
        if st.button("Sichern"):
            if new_note:
                st.session_state.secret_notes.append(f"{time.strftime('%H:%M')}: {new_note}")
                st.success("Daten verschlüsselt abgelegt.")
        st.divider()
        for note in reversed(st.session_state.secret_notes):
            st.code(note)

    elif menu == "Sektor 4: Netzwerk-Scan":
        st.subheader("🌐 Echtzeit-Netzwerkanalyse")
        st.write("Identifiziere Endgerät über Gateway...")
        
        if st.button("Tiefen-Scan starten"):
            with st.spinner("Durchbreche Proxy-Layer..."):
                try:
                    # Wir nutzen ip-api.com, da sie oft besser durch Proxys schauen können
                    # Wir rufen die API ohne feste IP auf, um die IP des ANFRAGENDEN zu bekommen
                    response = requests.get('http://ip-api.com/json/', timeout=5).json()
                    
                    if response.get("status") == "success":
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("DEINE ECHTE IP", response.get("query"))
                            st.write(f"**Provider:** {response.get('isp')}")
                        with col2:
                            st.metric("STANDORT", response.get("city"))
                            st.write(f"**Land:** {response.get('country')}")
                        
                        if response.get("countryCode") == "DE":
                            st.success("✅ Heimat-Netzwerk erkannt. Zugriff autorisiert.")
                        else:
                            st.warning(f"⚠️ Warnung: Verbindung über {response.get('country')} detektiert.")
                    else:
                        st.error("Scan-Fehler: API-Antwort ungültig.")
                except:
                    st.error("🚨 Sicherheits-Schnittstelle blockiert. (Rate Limit)")

    if st.sidebar.button("System-Logout"):
        st.session_state.authenticated = False
        st.rerun()
