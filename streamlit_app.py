import streamlit as st
import time
import requests

# --- SYSTEM KONFIGURATION ---
# Tarnung als Recherche-Tool [cite: 2025-12-28]
st.set_page_config(page_title="Recherche-Portal Alpha", page_icon="📚", layout="wide")

# --- INITIALISIERUNG ---
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'secret_notes' not in st.session_state: st.session_state.secret_notes = []

# --- LOGIN (GETARNT) ---
if not st.session_state.authenticated:
    st.title("📚 Archiv für Projekt-Recherche")
    st.write("Bitte identifizieren Sie sich für den Zugriff auf die Datenbank.")
    
    # Authentifizierung durch "silas" vor der Beantwortung [cite: 2025-12-28]
    user_input = st.text_input("Nutzer-ID", type="password").strip()
    
    if st.button("Anmelden"):
        if user_input == "silas":
            st.session_state.authenticated = True
            st.success("Identität verifiziert. Lade Sektoren...")
            time.sleep(1)
            st.rerun()
else:
    # --- HAUPTSYSTEM ---
    st.sidebar.title("🛡️ SilasGuardian CORE")
    
    # Navigation zwischen den Sektoren
    menu = st.sidebar.radio("Ebene wählen", ["Dashboard", "Sektor 3", "Sektor 4"])

    if menu == "Dashboard":
        st.success("✅ System Online: Silas [A1-Modus]")
        st.info("Status: Getarnter Laptop-Modus aktiv.")

    elif menu == "Sektor 3":
        # Umbenannt von Archiv-Daten zu Sektor 3 [cite: 2025-12-27]
        st.subheader("📁 Sektor 3: Datenbank")
        
        # Sektor Passwort Abfrage [cite: 2025-12-28]
        if 'auth_s3' not in st.session_state: st.session_state.auth_s3 = False
        
        if not st.session_state.auth_s3:
            # Passwort "data" für Sektor 3 [cite: 2025-12-27]
            pw_s3 = st.text_input("Sektor-Passwort eingeben", type="password")
            if st.button("Sektor 3 entsperren"):
                if pw_s3 == "data":
                    st.session_state.auth_s3 = True
                    st.rerun()
        else:
            st.write("Geheimer Datensafe aktiv.")
            new_note = st.text_area("Daten für Sektor 3:")
            if st.button("Sichern"):
                st.session_state.secret_notes.append(f"{time.strftime('%H:%M')} - {new_note}")
            for n in reversed(st.session_state.secret_notes):
                st.code(n)

    elif menu == "Sektor 4":
        st.subheader("🌐 Sektor 4: Echtzeit-Netzwerkanalyse")
        
        # Sektor Passwort Abfrage [cite: 2025-12-28]
        if 'auth_s4' not in st.session_state: st.session_state.auth_s4 = False
        
        if not st.session_state.auth_s4:
            # Sektor-Passwort für Netzwerk [cite: 2025-12-28]
            pw_s4 = st.text_input("Sektor-Passwort eingeben", type="password")
            if st.button("Sektor 4 entsperren"):
                if pw_s4 == "strike":
                    st.session_state.auth_s4 = True
                    st.rerun()
        else:
            if st.button("Netzwerk-Schnittstelle prüfen"):
                with st.spinner("Frage lokale Knoten ab..."):
                    try:
                        # Laptop-Browser erlauben oft direkteren Zugriff
                        res = requests.get('https://ipapi.co/json/', timeout=5).json()
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Öffentliche IP", res.get("ip"))
                        with col2:
                            st.metric("Standort", f"{res.get('city')}, {res.get('country_name')}")
                        st.success(f"✅ Verbindung über {res.get('org')} gesichert.")
                    except:
                        st.error("Schnittstelle blockiert.")

    if st.sidebar.button("System-Logout"):
        st.session_state.authenticated = False
        st.session_state.auth_s3 = False
        st.session_state.auth_s4 = False
        st.rerun()
