import streamlit as st
import time
from github import Github

# --- SYSTEM KONFIGURATION ---
st.set_page_config(page_title="Recherche-Portal Alpha", page_icon="🛡️", layout="wide")

# --- HILFSFUNKTIONEN FÜR GITHUB ---
def get_github_repo():
    try:
        token = st.secrets["GITHUB_TOKEN"]
        g = Github(token)
        # Dein spezifisches Repository
        return g.get_repo("plankton31012010-cell/SilasGuardianPro")
    except:
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

# --- INITIALISIERUNG ---
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 's3_auth' not in st.session_state: st.session_state.s3_auth = False

# --- LOGIN-SEKTOR ---
if not st.session_state.authenticated:
    st.title("🛡️ SilasGuardian | Core-Terminal")
    st.write("Identifizierung erforderlich für Systemstart (A1).")
    
    # Authentifizierung Silas [cite: 2025-12-28]
    master_key = st.text_input("Master-Key", type="password")
    
    if st.button("System hochfahren (A1)"):
        if master_key == "silas":
            st.session_state.authenticated = True
            log_event("SUCCESS: Silas logged in.")
            st.success("Authentifizierung erfolgreich. Lade Sektoren...")
            time.sleep(1)
            st.rerun()
        else:
            log_event(f"ALERT: Failed login attempt with key: {master_key}")
            st.error("Zugriff verweigert. Vorfall wurde permanent protokolliert.")

else:
    # --- HAUPTSYSTEM (MODUS A1) ---
    st.sidebar.title("🛡️ Control Center")
    st.sidebar.info(f"Status: Online | User: Silas")
    
    menu = st.sidebar.radio("Sektoren-Auswahl", 
                            ["Dashboard", "Sektor 0 (Falle)", "Sektor 3 (Archiv)", "Sektor 5 (Sentinel)"])

    # --- DASHBOARD ---
    if menu == "Dashboard":
        st.subheader("📊 System-Integrität & Logs")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Sicherheitsstatus", "OPTIMAL")
        with col2:
            if st.button("Permanente Audit-Logs laden"):
                repo = get_github_repo()
                if repo:
                    try:
                        logs = repo.get_contents("security_audit.txt").decoded_content.decode()
                        st.text_area("GitHub Audit-Trail:", logs, height=300)
                    except:
                        st.info("Noch keine Logs auf GitHub vorhanden.")

    # --- SEKTOR 0 (FALLE) ---
    elif menu == "Sektor 0 (Falle)":
        st.subheader("⚠️ Sektor Zero (Honey-Pot)")
        st.write("Komplexitätsgrad: Authentisch [cite: 2025-12-27]")
        st.code("""
        [08:42:11] TRACE: Connection from 192.168.1.1 rerouted.
        [08:42:15] DEBUG: Deploying False-Flag Archive...
        [08:42:19] STATUS: Intruder stuck in Sandbox Loop.
        """)
        st.warning("Dieser Sektor dient als Ablenkung für unbefugte Angreifer.")

    # --- SEKTOR 3 (DATA ARCHIV) ---
    elif menu == "Sektor 3 (Archiv)":
        st.subheader("📁 Sektor 3: Datenbank (Firmen-Vault)")
        
        if not st.session_state.s3_auth:
            # Sektor Passwort "data" [cite: 2025-12-27]
            s3_key = st.text_input("Sektor-Passwort erforderlich", type="password")
            if st.button("Sektor entsperren"):
                if s3_key == "data":
                    st.session_state.s3_auth = True
                    st.rerun()
                else:
                    st.error("Falsches Sektor-Passwort.")
        else:
            st.success("Verschlüsselter Kanal zu GitHub aktiv.")
            repo = get_github_repo()
            
            # Notizen laden
            try:
                note_file = repo.get_contents("sektor3_notes.txt")
                current_notes = note_file.decoded_content.decode()
            except:
                current_notes = "Hier deine Firmen-Ideen eintragen..."

            new_notes = st.text_area("Bearbeitungs-Terminal:", value=current_notes, height=350)
            
            if st.button("💾 Permanent auf GitHub speichern"):
                if repo:
                    try:
                        note_file = repo.get_contents("sektor3_notes.txt")
                        repo.update_file("sektor3_notes.txt", "Update Vault", new_notes, note_file.sha)
                        st.toast("Daten in Sektor 3 gesichert!", icon="✅")
                    except:
                        repo.create_file("sektor3_notes.txt", "Initial Vault", new_notes)
                        st.toast("Datei neu erstellt und gesichert!", icon="🚀")

            if st.button("Sektor 3 sperren"):
                st.session_state.s3_auth = False
                st.rerun()

    # --- SEKTOR 5 (SENTINEL) ---
    elif menu == "Sektor 5 (Sentinel)":
        st.subheader("📹 Sektor 5: Sensorik")
        st.camera_input("Manueller Scan-Trigger")

    # --- SHUTDOWN (A0) ---
    if st.sidebar.button("System herunterfahren (A0)"):
        st.session_state.authenticated = False
        st.session_state.s3_auth = False
        st.rerun()
