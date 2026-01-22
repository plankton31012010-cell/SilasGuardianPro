import streamlit as st
import time

# --- SYSTEM-KONFIGURATION ---
st.set_page_config(page_title="SilasGuardian", page_icon="🛡️", layout="wide")

class SilasGuardian:
    def __init__(self):
        # Speicher für den Systemstatus (bleibt bei Klicks erhalten)
        if 'auth_level' not in st.session_state:
            st.session_state.auth_level = "A0"
        if 'sectors' not in st.session_state:
            st.session_state.sectors = {
                0: {"name": "Sektor Zero", "status": "Deceptive/Authentic"},
                1: {"name": "Kern-System", "status": "Standby"},
                2: {"name": "Comms-Bridge", "status": "Standby"},
                3: {"name": "Sektor 3", "status": "Gesperrt"}
            }

    def startup_sequence(self):
        # Dynamische Überschrift und Begrüßung
        if st.session_state.auth_level == "A1+":
            st.title("Hallo Anton")
        else:
            st.title("SilasGuardian")

        st.info(f"Aktueller Systemstatus: {st.session_state.auth_level}")

        # Login-Bereich in der Seitenleiste
        with st.sidebar:
            st.header("Sicherheits-Check")
            ident = st.text_input("Ident-Bestätigung (silas)", type="password")
            pwd = st.text_input("Sektor-Passwort (data)", type="password")
            
            if st.button("System A1 Hochfahren"):
                # Prüfung der von dir festgelegten Parameter
                if ident.lower() == "silas" and pwd.lower() == "data":
                    st.session_state.auth_level = "A1+"
                    st.session_state.sectors[1]["status"] = "ONLINE"
                    st.session_state.sectors[2]["status"] = "ONLINE"
                    st.session_state.sectors[3]["status"] = "ENTSPERRT"
                    st.success("Autorisierung erfolgreich.")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Zugriff verweigert. Masterkey erforderlich?")

            if st.button("Shutdown (A0)"):
                st.session_state.auth_level = "A0"
                st.session_state.sectors[3]["status"] = "Gesperrt"
                st.rerun()

        # Status-Dashboard
        st.subheader("System-Integrität")
        cols = st.columns(4)
        for i, col in enumerate(cols):
            with col:
                status = st.session_state.sectors[i]["status"]
                st.metric(label=st.session_state.sectors[i]["name"], value=status)

        # Bereich für Sektor 3 (nur sichtbar wenn hochgefahren)
        if st.session_state.auth_level == "A1+":
            st.divider()
            st.header("📂 Zugriff: Sektor 3 - Archiv-Daten")
            st.success("Verbindung zu Sektor 3 stabil. Daten werden geladen...")
            st.write("Willkommen im gesicherten Bereich.")

# --- START ---
system = SilasGuardian()
system.startup_sequence()
