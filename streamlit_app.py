import streamlit as st
import time
from github import Github

# --- SYSTEM KONFIGURATION ---
st.set_page_config(page_title="SilasGuardian Terminal", page_icon="🛡️", layout="wide")

# --- GITHUB KOMMUNIKATIONS-KERN ---
def get_github_repo():
    try:
        # Greift auf den Token in deinen Streamlit-Secrets zu
        token = st.secrets["GITHUB_TOKEN"]
        g = Github(token)
        # WICHTIG: Prüfe, ob dieser Pfad exakt stimmt (Groß-/Kleinschreibung!)
        return g.get_repo("plankton31012010-cell/SilasGuardianPro")
    except Exception as e:
        st.error(f"Verbindungsfehler zu GitHub: {e}")
        return None

def log_event(message):
    repo = get_github_repo()
    if repo:
        path = "security_audit.txt"
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        new_entry = f"[{timestamp}] {message}\n"
        try:
            # Versuch, die Datei zu aktualisieren
            file = repo.get_contents(path)
            content = file.decoded_content.decode() + new_entry
            repo.update_file(path, "Audit Update", content, file.sha)
        except:
            # Falls Datei nicht existiert: Neu erstellen
            repo.create_file(path, "Audit Start", new_entry)

# --- SESSION STATE INITIALISIERUNG ---
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 's3_auth' not in st.session_state: st.session_state.s3_auth = False

# --- 1. LOGIN-SEKTOR ---
if not st.session_state.authenticated:
    st.title("🛡️ SilasGuardian | Core-Terminal")
    st.info("Systemstatus: Locked. Identifizierung für A1 erforderlich.")
    
    # Authentifizierung Silas [cite: 2025-12-28]
    master_key = st.text_input("Master-Key (Nutzer-ID)", type="password")
    
    if st.button("System hochfahren (A1)"):
        if master_key == "silas":
            st.session_state.authenticated = True
            log_event("SUCCESS: Silas angemeldet.")
            st.success("Identität bestätigt. Sektoren werden geladen...")
            time.sleep(1)
            st.rerun()
        else:
            log_event(f"ALERT: Falscher Key-Versuch: {master_key}")
            st.error("Zugriff verweigert. Protokoll wird an GitHub übertragen.")

else:
    # --- 2. HAUPTSYSTEM (MODUS A1) ---
    st.sidebar.title("🛡️ Control Center")
    st.sidebar.write(f"Sicherheits-Level: **Hoch**")
    
    menu = st.sidebar.radio("Sektoren-Auswahl", 
                            ["Dashboard", "Sektor 0 (Falle)", "Sektor 3 (Archiv)", "Sektor 5 (Sentinel)"])

    # --- DASHBOARD ---
    if menu == "Dashboard":
        st.subheader("📊 System-Status & Audit-Logs")
        st.write("Verbindung zu GitHub: ✅ Aktiv")
        
        if st.button("Logs von GitHub synchronisieren"):
            repo = get_github_repo()
            if repo:
                try:
                    logs = repo.get_contents("security_audit.txt").decoded_content.decode()
                    st.text_area("Permanente Historie (security_audit.txt):", logs, height=300)
                except:
                    st.info("Noch keine Log-Datei auf GitHub gefunden. Logge dich einmal falsch ein, um sie zu erstellen.")

    # --- SEKTOR 0 (DIE FALLE) ---
    elif menu == "Sektor 0 (Falle)":
        st.subheader("⚠️ Sektor Zero: Honey-Pot")
        st.warning("Eindringling-Täuschung aktiv [cite: 2025-12-27]")
        st.code("""
        [09:12:44] TRACE: Rerouting unauthorized packet...
        [09:12:48] ALERT: Intruder detected in false-loop 'Sector-Zero'.
        [09:12:52] INFO: Mirroring data to void-storage.
        """)
        st.write("Angreifer sehen hier nur wertlose Debug-Informationen.")

    # --- SEKTOR 3 (DEIN DATEN-SAFE) ---
    elif menu == "Sektor 3 (Archiv)":
        st.subheader("📁 Sektor 3: Datenbank (Firmen-Planung)")
        
        if not st.session_state.s3_auth:
            # Sektor Passwort "data" [cite: 2025-12-27]
            s3_key = st.text_input("Sektor-Passwort (Sector-Key)", type="password")
            if st.button("Sektor entsperren"):
                if s3_key == "data":
                    st.session_state.s3_auth = True
                    st.rerun()
                else:
                    st.error("Falsches Sektor-Passwort!")
        else:
            st.success("Verschlüsselter Kanal zu Sektor 3 aktiv.")
            repo = get_github_repo()
            
            # Notizen laden
            path_s3 = "sektor3_notes.txt"
            try:
                note_file = repo.get_contents(path_s3)
                current_notes = note_file.decoded_content.decode()
            except:
                current_notes = "Hier deine Firmen-Ideen und Sparpläne eintragen..."

            new_notes = st.text_area("Bearbeitungs-Terminal:", value=current_notes, height=400)
            
            if st.button("💾 Permanent auf GitHub speichern"):
                if repo:
                    try:
                        # Prüfen ob Datei existiert für Update
                        try:
                            note_file = repo.get_contents(path_s3)
                            repo.update_file(path_s3, "Update Vault Content", new_notes, note_file.sha)
                        except:
                            # Wenn nicht, neu erstellen
                            repo.create_file(path_s3, "Initial Vault Creation", new_notes)
                        st.success("✅ Erfolgreich in der Cloud gesichert!")
                    except Exception as e:
                        st.error(f"Fehler beim Speichern: {e}")

            if st.button("Sektor 3 sperren"):
                st.session_state.s3_auth = False
                st.rerun()

    # --- SEKTOR 5 (SENTINEL) ---
    elif menu == "Sektor 5 (Sentinel)":
        st.subheader("📹 Sektor 5: Sensorik")
        st.camera_input("Manueller Scan-Trigger (Sentinel-Cam)")

    # --- SHUTDOWN (A0) ---
    if st.sidebar.button("System herunterfahren (A0)"):
        st.session_state.authenticated = False
        st.session_state.s3_auth = False
        st.info("System wird heruntergefahren...")
        time.sleep(1)
        st.rerun()
