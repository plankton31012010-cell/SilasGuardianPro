import streamlit as st
import time
from github import Github

# --- 1. SYSTEM KONFIGURATION ---
st.set_page_config(page_title="SilasGuardian Terminal", page_icon="🛡️", layout="wide")

# --- 2. GITHUB FUNKTIONEN ---
def get_github_repo():
    try:
        # Sucht in den Streamlit Secrets nach GITHUB_TOKEN
        token = st.secrets["GITHUB_TOKEN"]
        g = Github(token)
        # Pfad: Benutzername/Repository-Name
        return g.get_repo("plankton31012010-cell/SilasGuardianPro")
    except Exception as e:
        return None

def log_event(message):
    repo = get_github_repo()
    if repo:
        path = "security_audit.txt"
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        new_entry = f"[{timestamp}] {message}\n"
        try:
            file = repo.get_contents(path)
            content = file.decoded_content.decode() + new_entry
            repo.update_file(path, "Audit Update", content, file.sha)
        except:
            repo.create_file(path, "Audit Start", new_entry)

# --- 3. SESSION INITIALISIERUNG ---
if 'authenticated' not in st.session_state: 
    st.session_state.authenticated = False
if 's3_auth' not in st.session_state: 
    st.session_state.s3_auth = False

# --- 4. LOGIN-BEREICH ---
if not st.session_state.authenticated:
    st.title("🛡️ SilasGuardian | Core-Terminal")
    st.info("Systemstatus: Sperre aktiv. Identifizierung für Modus A1 erforderlich.")
    
    master_key = st.text_input("Master-Key eingeben", type="password")
    
    if st.button("System starten (A1)"):
        if master_key == "silas":
            st.session_state.authenticated = True
            log_event("SUCCESS: Login durch Silas.")
            st.success("Zugriff gewährt.")
            st.rerun()
        else:
            log_event(f"ALERT: Unbefugter Versuch mit Key: {master_key}")
            st.error("Zugriff verweigert. Vorfall protokolliert.")

else:
    # --- 5. HAUPTSYSTEM (MODUS A1) ---
    st.sidebar.title("🛡️ Menü")
    menu = st.sidebar.radio("Sektoren", ["Dashboard", "Sektor 0 (Falle)", "Sektor 3 (Archiv)", "Sektor 5 (Sentinel)"])

    # --- DASHBOARD ---
    if menu == "Dashboard":
        st.subheader("📊 System-Status")
        st.write("Verbindung zu GitHub: **Aktiv**")
        
        if st.button("Audit-Logs von GitHub laden"):
            repo = get_github_repo()
            if repo:
                try:
                    logs = repo.get_contents("security_audit.txt").decoded_content.decode()
                    st.text_area("Protokoll-Datei:", logs, height=250)
                except:
                    st.info("Noch keine Protokolle vorhanden.")

    # --- SEKTOR 0 ---
    elif menu == "Sektor 0 (Falle)":
        st.subheader("⚠️ Sektor Zero")
        st.warning("Honey-Pot aktiv. Täusche Angreifer vor...")
        st.code("ERROR 403: Redirecting to Virtual Sandbox...")

    # --- SEKTOR 3 (DATA-SAFE) ---
    elif menu == "Sektor 3 (Archiv)":
        st.subheader("📁 Sektor 3: Datenbank")
        
        if not st.session_state.s3_auth:
            s3_key = st.text_input("Sektor-Passwort", type="password")
            if st.button("Sektor öffnen"):
                if s3_key == "data":
                    st.session_state.s3_auth = True
                    st.rerun()
                else:
                    st.error("Sektor-Key ungültig.")
        else:
            repo = get_github_repo()
            path_s3 = "sektor3_notes.txt"
            
            try:
                note_file = repo.get_contents(path_s3)
                current_notes = note_file.decoded_content.decode()
            except:
                current_notes = "Erstelle deine erste Notiz..."

            new_notes = st.text_area("Inhalt bearbeiten:", value=current_notes, height=300)
            
            if st.button("💾 Speichern"):
                if repo:
                    try:
                        try:
                            note_file = repo.get_contents(path_s3)
                            repo.update_file(path_s3, "S3 Update", new_notes, note_file.sha)
                        except:
                            repo.create_file(path_s3, "S3 Init", new_notes)
                        st.success("In Cloud gesichert!")
                    except Exception as e:
                        st.error(f"Fehler: {e}")

            if st.button("Sektor wieder sperren"):
                st.session_state.s3_auth = False
                st.rerun()

    # --- SEKTOR 5 ---
    elif menu == "Sektor 5 (Sentinel)":
        st.subheader("📹 Sentinel-Kamera")
        st.camera_input("Live-Scan")

    # --- SHUTDOWN ---
    if st.sidebar.button("Herunterfahren (A0)"):
        st.session_state.authenticated = False
        st.session_state.s3_auth = False
        st.rerun()
