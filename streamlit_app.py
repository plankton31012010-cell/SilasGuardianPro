import streamlit as st
import os
import time

# --- KONFIGURATION & PERSISTENZ ---
st.set_page_config(page_title="SilasGuardian", page_icon="🛡️", layout="wide")
SAVE_DIR = "sector_3_vault"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

class SilasGuardian:
    def __init__(self):
        if 'auth_level' not in st.session_state:
            st.session_state.auth_level = "A0"
        if 'page' not in st.session_state:
            st.session_state.page = "login"

    def logout(self):
        st.session_state.auth_level = "A0"
        st.session_state.page = "login"
        st.rerun()

    def render(self):
        # --- 1. LOGIN SEITE ---
        if st.session_state.auth_level == "A0":
            st.title("🛡️ SilasGuardian | Systemzugang")
            st.divider()
            col1, col2 = st.columns(2)
            ident = col1.text_input("Ident-Key", type="password")
            pwd = col2.text_input("Sektor-Passwort", type="password")
            
            if st.button("System initialisieren"):
                if ident.lower() == "silas" and pwd.lower() == "data":
                    st.session_state.auth_level = "A1+"
                    st.session_state.page = "dashboard"
                    st.success("Autorisierung erfolgreich.")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Zugriff verweigert.")
            return

        # --- 2. DAS NEUE DASHBOARD (STARTSEITE NACH LOGIN) ---
        if st.session_state.page == "dashboard":
            st.title("Hallo Anton")
            st.subheader("Willkommen im SilasGuardian Hauptquartier")
            st.info("Systemstatus: ONLINE (Modus A1+)")
            
            st.write("Wähle ein Modul aus der Übersicht:")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📡 Netzwerk-Scanner öffnen", use_container_width=True):
                    st.session_state.page = "scanner"
                    st.rerun()
            with col2:
                if st.button("📂 Sektor 3 (Datentresor)", use_container_width=True):
                    st.session_state.page = "vault"
                    st.rerun()
            with col3:
                if st.button("🛡️ Sektor Zero", use_container_width=True):
                    st.session_state.page = "honeypot"
                    st.rerun()

            st.divider()
            if st.button("🚨 SYSTEM SHUTDOWN", type="primary", use_container_width=True):
                self.logout()

        # --- 3. MODUL: NETZWERK-SCANNER ---
        elif st.session_state.page == "scanner":
            st.title("📡 Netzwerk-Scanner")
            if st.button("← Zurück zum Dashboard"):
                st.session_state.page = "dashboard"
                st.rerun()
            st.write("Scanner-Logik aktiv...")
            # Hier kommt dein Scan-Code rein

        # --- 4. MODUL: SEKTOR 3 (MIT SPEICHER-FUNKTION) ---
        elif st.session_state.page == "vault":
            st.title("📂 Sektor 3: Sicherer Datentresor")
            if st.button("← Zurück zum Dashboard"):
                st.session_state.page = "dashboard"
                st.rerun()
            
            up = st.file_uploader("Datei dauerhaft speichern")
            if up:
                with open(os.path.join(SAVE_DIR, up.name), "wb") as f:
                    f.write(up.getbuffer())
                st.success(f"'{up.name}' wurde physikalisch in Sektor 3 gespeichert.")

            st.divider()
            st.subheader("Archivierte Dateien (Persistent)")
            files = os.listdir(SAVE_DIR)
            if files:
                for f in files:
                    col_f, col_d = st.columns([4, 1])
                    col_f.write(f"🔒 {f}")
                    with open(os.path.join(SAVE_DIR, f), "rb") as file_bytes:
                        col_d.download_button("Öffnen", data=file_bytes, file_name=f, key=f)
            else:
                st.write("Keine Daten gefunden.")

        # --- 5. MODUL: SEKTOR ZERO ---
        elif st.session_state.page == "honeypot":
            st.title("🛡️ Sektor Zero: Honey-Pot")
            if st.button("← Zurück zum Dashboard"):
                st.session_state.page = "dashboard"
                st.rerun()
            st.toggle("Täuschungsprotokoll aktiv")

# --- START ---
if __name__ == "__main__":
    SilasGuardian().render()
