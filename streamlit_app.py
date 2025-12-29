import streamlit as st
import time

# --- SYSTEM KONFIGURATION ---
st.set_page_config(page_title="Recherche-Portal Alpha", page_icon="📚", layout="wide")

# --- INITIALISIERUNG ---
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'sentinel_logs' not in st.session_state: st.session_state.sentinel_logs = []
if 'intruder_images' not in st.session_state: st.session_state.intruder_images = []

# --- LOGIN-BEREICH MIT FALLE ---
if not st.session_state.authenticated:
    st.title("📚 Projekt-Archiv")
    st.write("Identifizierung erforderlich.")
    
    # Das Eingabefeld für den Master-Key [cite: 2025-12-28]
    user_input = st.text_input("Nutzer-ID", type="password").strip()
    
    # VERSTECKTE FALLE: Wenn das Passwort falsch ist, wird dieses Feld aktiv
    capture_intruder = st.camera_input("⚠️ Sicherheitsscan zur Verifizierung erforderlich (Bitte in die Kamera blicken)")

    if st.button("Anmelden"):
        if user_input == "silas":
            st.session_state.authenticated = True
            st.session_state.sentinel_logs.append(f"🟢 {time.strftime('%H:%M:%S')} - Silas angemeldet.")
            st.rerun()
        else:
            # Wenn das Passwort falsch war UND ein Bild gemacht wurde
            if capture_intruder:
                st.session_state.intruder_images.append({
                    "time": time.strftime('%H:%M:%S'),
                    "image": capture_intruder
                })
            st.session_state.sentinel_logs.append(f"🔴 {time.strftime('%H:%M:%S')} - ILLEGALER ZUGRIFFSVERSUCH")
            st.error("Identität konnte nicht bestätigt werden. Vorfall wurde protokolliert.")

else:
    # --- HAUPTSYSTEM ---
    st.sidebar.title("🛡️ Core Control")
    menu = st.sidebar.radio("Sektoren", ["Dashboard", "Sektor 0 (Falle)", "Sektor 3 (Vault)", "Sektor 5 (Sentinel)"])

    if menu == "Dashboard":
        st.success("✅ System Online: Silas")
        
        # ECHTER NUTZEN: Identifizierung von Eindringlingen
        st.write("### 🚨 Eindringling-Identifizierung")
        if not st.session_state.intruder_images:
            st.info("Keine unbefugten Personen detektiert.")
        else:
            for attempt in reversed(st.session_state.intruder_images):
                st.warning(f"Eindringling erfasst um {attempt['time']}")
                st.image(attempt['image'], width=300)
        
        st.divider()
        st.write("### 📜 System-Logs")
        for log in reversed(st.session_state.sentinel_logs):
            st.text(log)

    elif menu == "Sektor 0 (Falle)":
        # Authentisches Sektor 0 [cite: 2025-12-27]
        st.subheader("⚠️ Sektor Zero")
        st.code("DEBUG: Redirecting unauthorized IP to Black-Hole-Server...")

    elif menu == "Sektor 3 (Vault)":
        # Passwort "data" erforderlich [cite: 2025-12-27]
        st.subheader("🔐 Sektor 3: Datenbank")
        if st.text_input("Sektor-Key", type="password") == "data":
            st.write("Tresorinhalt wird geladen...")

    elif menu == "Sektor 5 (Sentinel)":
        st.subheader("📹 Manuelle Überwachung")
        st.camera_input("Scanner-Sicht")

    if st.sidebar.button("System-Logout"):
        st.session_state.authenticated = False
        st.rerun()
