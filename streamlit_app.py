import streamlit as st
import time
from github import Github

# --- SYSTEM KONFIGURATION ---
st.set_page_config(page_title="Recherche-Portal Alpha", page_icon="📚")

# --- GITHUB INTEGRATION (Permanent Logs) ---
def log_to_github(message):
    try:
        token = st.secrets["GITHUB_TOKEN"]
        g = Github(token)
        repo = g.get_repo("plankton31012010-cell/SilasGuardianPro")
        
        # Holt das bestehende Log oder erstellt ein neues
        file_path = "security_audit.txt"
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        new_content = f"[{timestamp}] {message}\n"
        
        try:
            file = repo.get_contents(file_path)
            existing_content = file.decoded_content.decode()
            repo.update_file(file_path, "Update Log", existing_content + new_content, file.sha)
        except:
            repo.create_file(file_path, "Initial Log", new_content)
        return True
    except:
        return False

# --- SESSION STATE ---
if 'authenticated' not in st.session_state: st.session_state.authenticated = False

# --- LOGIN-BEREICH ---
if not st.session_state.authenticated:
    st.title("📚 Projekt-Archiv | Login")
    
    # Authentifizierung Silas [cite: 2025-12-28]
    master_key = st.text_input("Master-Key eingeben", type="password")
    
    if st.button("System starten"):
        if master_key == "silas":
            st.session_state.authenticated = True
            log_to_github("SUCCESS: Silas logged in.")
            st.rerun()
        else:
            log_to_github(f"FAILED: Unauthorized attempt with key '{master_key}'")
            st.error("Zugriff verweigert. Vorfall wurde protokolliert.")

else:
    # --- HAUPTSYSTEM (A1 Modus) ---
    st.sidebar.title("🛡️ Core Control")
    
    menu = st.sidebar.radio("Navigation", ["Dashboard", "Sektor 0 (Falle)", "Sektor 3 (Data)", "Sektor 5 (Sentinel)"])

    if menu == "Dashboard":
        st.subheader("📊 System-Status & Audit-Logs")
        st.success("System-Integrität: OK")
        
        # Anzeige der permanenten Logs direkt aus GitHub
        if st.button("Logs von GitHub laden"):
            try:
                token = st.secrets["GITHUB_TOKEN"]
                g = Github(token)
                repo = g.get_repo("plankton31012010-cell/SilasGuardianPro")
                content = repo.get_contents("security_audit.txt").decoded_content.decode()
                st.text_area("Permanente Historie:", content, height=300)
            except:
                st.info("Noch keine permanenten Logs verfügbar.")

    elif menu == "Sektor 0 (Falle)":
        st.subheader("⚠️ Sektor Zero")
        st.code("DEBUG: Redirecting unauthorized IP to Black-Hole-Server...")
        st.warning("Eindringling-Täuschung aktiv.")

    elif menu == "Sektor 3 (Data)":
        # Sektor Passwort "data" [cite: 2025-12-27]
        st.subheader("📁 Sektor 3: Datenbank")
        if st.text_input("Sektor-Key", type="password") == "data":
            st.write("Sichere Notizen hier ablegen...")
            # Hier könnte man eine Textdatei auf GitHub speichern

    elif menu == "Sektor 5 (Sentinel)":
        st.subheader("📹 Manuelle Überwachung")
        st.write("Kamera nur bei Bedarf aktivieren.")
        st.camera_input("Live-Scanner")

    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()
