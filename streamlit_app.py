import streamlit as st
import time
import requests

# --- SYSTEM KONFIGURATION ---
st.set_page_config(page_title="SilasGuardian CORE v12.3", page_icon="🛡️", layout="wide")

# --- INITIALISIERUNG ---
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'failed_attempts' not in st.session_state: st.session_state.failed_attempts = 0
if 'lockout_time' not in st.session_state: st.session_state.lockout_time = 0

# --- LOCKDOWN-CHECK ---
if st.session_state.lockout_time > time.time():
    st.error(f"🚨 LOCKDOWN: Zugriff gesperrt.")
    st.stop()

# --- LOGIN ---
if not st.session_state.authenticated:
    st.title("🔐 SilasGuardian | Login")
    user_input = st.text_input("Master-Key", type="password").strip()
    if st.button("Unlock"):
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
    st.sidebar.title("🛡️ Core")
    menu = st.sidebar.radio("Sektor", ["Dashboard", "Sektor 4: External Scan"])

    if menu == "Dashboard":
        st.success("✅ System Online: Silas")
        st.info("Scanner-Schnittstelle bereit.")

    elif menu == "Sektor 4: External Scan":
        st.subheader("🌐 Netzwerkanalyse (Echtzeit)")
        if st.button("Scan starten"):
            with st.spinner("Frage echte Netzwerk-Daten ab..."):
                try:
                    # Holt deine echte öffentliche IP und Daten
                    r = requests.get('https://ipapi.co/json/')
                    data = r.json()
                    st.metric("Öffentliche IP-Adresse", data.get("ip"))
                    st.write(f"**Anbieter:** {data.get('org')}")
                    st.write(f"**Region:** {data.get('city')}, {data.get('country_name')}")
                    st.success("Schnittstelle sicher.")
                except:
                    st.error("API blockiert.")

    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()
