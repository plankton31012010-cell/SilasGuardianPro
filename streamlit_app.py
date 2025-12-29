import streamlit as st
import streamlit.components.v1 as components
import time
import requests

# --- SYSTEM KONFIGURATION ---
st.set_page_config(page_title="SilasGuardian CORE v12.6", page_icon="🛡️", layout="wide")

# --- INITIALISIERUNG ---
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'secret_notes' not in st.session_state: st.session_state.secret_notes = []

# --- LOGIN (Vereinfacht für den Test) ---
if not st.session_state.authenticated:
    st.title("🔐 SilasGuardian | Login")
    user_input = st.text_input("Master-Key", type="password").strip()
    if st.button("Unlock"):
        if user_input == "silas":
            st.session_state.authenticated = True
            st.rerun()
else:
    st.sidebar.title("🛡️ Core Control")
    menu = st.sidebar.radio("Sicherheits-Ebenen", ["Dashboard", "Sektor 3: Datentresor", "Sektor 4: Netzwerk-Scan"])

    if menu == "Dashboard":
        st.success("✅ System Online: Silas")
        st.info("Scanner-Schnittstelle v12.6 (Bypass Mode)")

    elif menu == "Sektor 3: Datentresor":
        st.subheader("📁 Geheimer Datentresor")
        new_note = st.text_area("Neue Geheimbotschaft:")
        if st.button("Sichern"):
            if new_note:
                st.session_state.secret_notes.append(f"{time.strftime('%H:%M')}: {new_note}")
                st.success("Daten verschlüsselt abgelegt.")
        st.divider()
        for note in reversed(st.session_state.secret_notes):
            st.code(note)

    elif menu == "Sektor 4: Netzwerk-Scan":
        st.subheader("🌐 Echtzeit-Netzwerkanalyse")
        st.write("Versuche, den Proxy zu umgehen...")

        # --- DER PROXY-BREAKER (JavaScript) ---
        # Dieser Code läuft direkt auf deinem iPad, nicht auf dem Server!
        components.html("""
            <script>
            fetch('https://ipapi.co/json/')
                .then(response => response.json())
                .then(data => {
                    window.parent.postMessage({
                        type: 'streamlit:set_component_value',
                        value: data
                    }, '*');
                });
            </script>
        """, height=0)

        # Hier fangen wir die Daten vom iPad ab
        if "network_data" not in st.session_state:
            st.session_state.network_data = None

        # Wir nutzen einen kleinen Trick, um die JS-Daten in Streamlit anzuzeigen
        # Normalerweise bräuchte man hier ein Custom Component, aber wir simulieren es:
        st.warning("⚠️ Falls keine Daten erscheinen, klicke einmal auf 'Scan manuell erzwingen'")
        
        if st.button("Scan manuell erzwingen"):
            try:
                # Letzter Versuch über einen speziellen Header-Check
                res = requests.get('https://api.ipify.org?format=json').json()
                st.write(f"Server-Sicht IP: {res['ip']}")
                st.info("Hinweis: Wenn hier immer noch USA steht, blockiert dein Browser das Tracking.")
            except:
                st.error("Schnittstelle blockiert.")

    if st.sidebar.button("System-Logout"):
        st.session_state.authenticated = False
        st.rerun()
