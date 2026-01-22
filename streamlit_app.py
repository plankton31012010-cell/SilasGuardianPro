import streamlit as st
import time

# --- SYSTEM-KONFIGURATION ---
st.set_page_config(page_title="SilasGuardian", page_icon="🛡️", layout="wide")

class SilasGuardian:
    def __init__(self):
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
        # Dynamische Überschrift
        if st.session_state.auth_level == "A1+":
            st.title("Hallo Anton")
        else:
            st.title("SilasGuardian")

        st.info(f"Aktueller Systemstatus: {st.session_state.auth_level}")

        # Login-Bereich in der Seitenleiste (Passwörter entfernt)
        with st.sidebar:
            st.header("Sicherheits-Check")
            # Die Bezeichnungen in den Klammern wurden entfernt
            ident = st.text_input("Ident-Bestätigung", type="password", placeholder="Eingabe erforderlich...")
            pwd = st.text_input("Sektor-Passwort", type="password", placeholder="Eingabe erforderlich...")
            
            if st.button("System A1 Hochfahren"):
                # Interne Prüfung ohne Anzeige der Werte auf der UI
                if ident.lower() == "silas" and pwd.lower() == "data":
                    st.session_state.auth_level = "A1+"
                    st.session_state.sectors[1]["status"] = "ONLINE"
                    st.session_state.sectors[2]["status"] = "ONLINE"
                    st.session_state.sectors[3]["status"] = "ENTSPERRT"
                    st.success("Autorisierung erfolgreich.")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Zugriff verweigert.")

            if st.button("Shutdown (A0)"):
                st.session_state.auth_level = "A0"
                st.rerun()

        # Dashboard
        st.subheader("System-Integrität")
        cols = st.columns(4)
        for i, col in enumerate(cols):
            with col:
                st.metric(label=st.session_state.sectors[i]["name"], 
                          value=st.session_state.sectors[i]["status"])

# --- START ---
system = SilasGuardian()
system.startup_sequence()
