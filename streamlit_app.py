import streamlit as st
import time

# --- SYSTEM KONFIGURATION ---
st.set_page_config(page_title="Recherche-Portal Alpha", page_icon="📚", layout="wide")

# --- INITIALISIERUNG ---
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'vault' not in st.session_state: st.session_state.vault = []
if 'sentinel_logs' not in st.session_state: st.session_state.sentinel_logs = []
if 'failed_attempts' not in st.session_state: st.session_state.failed_attempts = 0

# --- PANIC FUNKTION ---
def trigger_panic():
    js = "window.location.href = 'https://gemini.google.com';"
    st.components.v1.html(f"<script>{js}</script>", height=0)
    st.session_state.authenticated = False
    st.stop()

# --- LOGIN (Ident-Wort: silas [cite: 2025-12-28]) ---
if not st.session_state.authenticated:
    st.title("📚 Projekt-Archiv")
    st.write("Bitte identifizieren Sie sich für den Zugriff.")
    user_input = st.text_input("Nutzer-ID", type="password").strip()
    
    if st.button("Anmelden"):
        if user_input == "silas":
            st.session_state.authenticated = True
            st.session_state.sentinel_logs.append(f"🟢 {time.strftime('%H:%M:%S')} - Autorisierter Zugriff (Silas)")
            st.rerun()
        else:
            st.session_state.failed_attempts += 1
            st.session_state.sentinel_logs.append(f"🔴 {time.strftime('%H:%M:%S')} - FEHLVERSUCH")
            st.error("Zugriff verweigert.")
else:
    # --- HAUPTSYSTEM (A1 Modus [cite: 2025-12-27]) ---
    st.sidebar.title("🛡️ SilasGuardian CORE")
    
    if st.sidebar.button("🆘 PANIC-MODE"):
        trigger_panic()

    menu = st.sidebar.radio("Sektoren", ["Dashboard", "Sektor 0 (Defense)", "Sektor 3 (Vault)", "Sektor 5 (Sentinel)"])

    if menu == "Dashboard":
        st.success("✅ System Online: Silas")
        st.write("### 📜 System- & Überwachungs-Logs")
        if not st.session_state.sentinel_logs:
            st.write("Keine Aktivitäten aufgezeichnet.")
        else:
            for log in reversed(st.session_state.sentinel_logs):
                st.text(log)
        
        if st.session_state.failed_attempts >= 3:
            st.warning("⚠️ Warnung: Mehrere Fehlversuche registriert!")

    elif menu == "Sektor 0 (Defense)":
        # Komplexe falsche Fährte [cite: 2025-12-27]
        st.subheader("⚠️ Sektor Zero: Honey-Pot Protokoll")
        st.code("""
        [SCAN] Analyzing incoming packets...
        [ALERT] Spoofed IP detected: 192.x.x.x
        [ACTION] Deploying Virtual-Trap-Node...
        [STATUS] Intruder isolated in Sandbox.
        """)

    elif menu == "Sektor 3 (Vault)":
        # Passwort "data" erforderlich [cite: 2025-12-27]
        st.subheader("🔐 Sektor 3: Datenbank")
        pw_s3 = st.text_input("Sektor-Passwort", type="password")
        if pw_s3 == "data":
            st.info("Flüchtiger Tresor aktiv.")
            new_note = st.text_input("Eintrag sichern:")
            if st.button("Speichern"):
                st.session_state.vault.append(f"{time.strftime('%H:%M')} - {new_note}")
            for n in reversed(st.session_state.vault):
                st.code(n)

    elif menu == "Sektor 5 (Sentinel)":
        # Physische Überwachung
        st.subheader("📹 Sektor 5: Sentinel-Kamera")
        st.write("Nutze dieses Terminal zur Raum-Überwachung.")
        
        cam_image = st.camera_input("Kamera-Schnittstelle")
        if cam_image:
            st.session_state.sentinel_logs.append(f"📸 {time.strftime('%H:%M:%S')} - Überwachungsbild aufgenommen")
            st.image(cam_image, caption="Letzte Aufnahme")
            st.success("Bild-Ereignis im Log registriert.")

    if st.sidebar.button("System-Logout"):
        st.session_state.authenticated = False
        st.rerun()
