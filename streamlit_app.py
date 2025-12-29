import streamlit as st
import time
import requests

# --- SYSTEM KONFIGURATION ---
# Tarnung als Recherche-Tool [cite: 2025-12-28]
st.set_page_config(page_title="Recherche-Portal Alpha", page_icon="📚", layout="wide")

# --- PANIC LOGIK (JavaScript) ---
def trigger_panic():
    # Öffnet Gemini in einem neuen Fenster und leitet den aktuellen Tab auf Google um
    js = "window.open('https://gemini.google.com', '_blank'); window.location.href = 'https://www.google.com/search?q=geschichte+hausarbeit+quellen';"
    st.components.v1.html(f"<script>{js}</script>", height=0)
    st.session_state.authenticated = False # Loggt dich sofort aus [cite: 2025-12-28]

# --- INITIALISIERUNG ---
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'secret_notes' not in st.session_state: st.session_state.secret_notes = []

# --- PANIC BUTTON IN DER SIDEBAR ---
if st.sidebar.button("🆘 PANIC: Forschungs-Modus"):
    trigger_panic()
    st.stop()

# --- LOGIN (GETARNT) ---
if not st.session_state.authenticated:
    st.title("📚 Archiv für Projekt-Recherche")
    st.write("Bitte identifizieren Sie sich für den Zugriff auf die Datenbank.")
    
    # Authentifizierung durch "silas" [cite: 2025-12-28]
    user_input = st.text_input("Nutzer-ID", type="password").strip()
    
    if st.button("Anmelden"):
        if user_input == "silas":
            st.session_state.authenticated = True
            st.rerun()
else:
    # --- HAUPTSYSTEM ---
    st.sidebar.title("🛡️ Core Control")
    menu = st.sidebar.radio("Ebene wählen", ["Dashboard", "Sektor 3", "Sektor 4"])

    if menu == "Dashboard":
        st.success("✅ System Online: Silas [A1-Modus] [cite: 2025-12-27]")
        st.info("Status: Laptop-Schnittstelle verifiziert.")

    elif menu == "Sektor 3":
        # Sektor 3 autorisiert mit "data" [cite: 2025-12-27]
        st.subheader("📁 Sektor 3: Datenbank")
        if 'auth_s3' not in st.session_state: st.session_state.auth_s3 = False
        
        if not st.session_state.auth_s3:
            pw_s3 = st.text_input("Sektor-Passwort", type="password")
            if st.button("Sektor 3 entsperren"):
                if pw_s3 == "data":
                    st.session_state.auth_s3 = True
                    st.rerun()
        else:
            st.write("Geheimer Datensafe aktiv.")
            for n in reversed(st.session_state.secret_notes):
                st.code(n)

    elif menu == "Sektor 4":
        # Sektor 4 autorisiert mit "strike" [cite: 2025-12-28]
        st.subheader("🌐 Sektor 4: Netzwerk-Scan")
        if 'auth_s4' not in st.session_state: st.session_state.auth_s4 = False
        
        if not st.session_state.auth_s4:
            pw_s4 = st.text_input("Netzwerk-Passwort", type="password")
            if st.button("Sektor 4 entsperren"):
                if pw_s4 == "strike":
                    st.session_state.auth_s4 = True
                    st.rerun()
        else:
            if st.button("Netzwerk prüfen"):
                res = requests.get('https://ipapi.co/json/').json()
                st.metric("Öffentliche IP", res.get("ip"))
                st.write(f"**Standort:** {res.get('city')}, {res.get('country_name')}")

    if st.sidebar.button("System-Logout"):
        st.session_state.authenticated = False
        st.rerun()
