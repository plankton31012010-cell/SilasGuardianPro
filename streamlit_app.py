import streamlit as st
import time
from github import Github
import base64

# --- SYSTEM KONFIGURATION ---
st.set_page_config(page_title="Recherche-Portal Alpha", page_icon="📚")

# --- GITHUB INTEGRATION ---
# Holt sich den Token sicher aus den Streamlit Secrets
try:
    token = st.secrets["GITHUB_TOKEN"]
    g = Github(token)
    repo = g.get_repo("plankton31012010-cell/SilasGuardianPro")
except:
    st.error("⚠️ GitHub-Token fehlt in den Secrets!")

def upload_to_github(image_data, filename):
    try:
        path = f"intruders/{filename}"
        repo.create_file(path, f"Audit: {filename}", image_data, branch="main")
        return True
    except:
        return False

# --- LOGIN ---
if 'authenticated' not in st.session_state: st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🛡️ SilasGuardian | Bio-Vault")
    master_key = st.text_input("Master-Key", type="password")
    bio_scan = st.camera_input("Identitäts-Abgleich")

    if st.button("System entsperren"):
        if master_key == "silas":
            st.session_state.authenticated = True
            st.rerun()
        else:
            if bio_scan:
                # Bild für den Upload vorbereiten
                img_bytes = bio_scan.getvalue()
                fname = f"intruder_{time.strftime('%Y%m%d_%H%M%S')}.png"
                if upload_to_github(img_bytes, fname):
                    st.error("🔒 Zugriff verweigert. Biometrie permanent archiviert.")
                else:
                    st.error("🔒 Zugriff verweigert. Backup-Fehler.")
            else:
                st.warning("⚠️ Biometrie-Scan erforderlich für Protokollierung.")

else:
    st.sidebar.title("🛡️ Core Control")
    menu = st.sidebar.radio("Sektoren", ["Dashboard", "Sektor 0", "Sektor 3"])

    if menu == "Dashboard":
        st.subheader("🕵️ Permanente Beweissicherung")
        st.write("Hier werden die Bilder direkt aus deinem GitHub-Ordner geladen:")
        
        try:
            contents = repo.get_contents("intruders")
            for file in reversed(contents):
                st.image(file.download_url, caption=f"Erfasst am: {file.name}", width=300)
        except:
            st.info("Noch keine Beweisbilder im permanenten Speicher.")

    # ... Sektor 3 Logik bleibt gleich ...
