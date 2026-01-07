import streamlit as st
from github import Github

st.title("🛡️ SilasGuardian Debug-Modus")

# PRÜFUNG DER SECRETS
st.subheader("1. Secrets-Check")
if "GITHUB_TOKEN" in st.secrets:
    st.success("✅ 'GITHUB_TOKEN' wurde in den Secrets gefunden!")
    # Wir zeigen nur die ersten 4 Zeichen zur Sicherheit
    token_anfang = st.secrets["GITHUB_TOKEN"][:4]
    st.write(f"Dein Token beginnt mit: `{token_anfang}` (Sollte 'ghp_' sein)")
else:
    st.error("❌ 'GITHUB_TOKEN' wurde NICHT gefunden. Prüfe die Schreibweise in den Secrets!")

# PRÜFUNG DER VERBINDUNG
st.subheader("2. GitHub-Verbindung")
try:
    token = st.secrets["GITHUB_TOKEN"]
    g = Github(token)
    repo = g.get_repo("plankton31012010-cell/SilasGuardianPro")
    st.success(f"✅ Verbindung zu Repository '{repo.full_name}' erfolgreich!")
except Exception as e:
    st.error(f"❌ GitHub-Fehler: {e}")

# SPEICHER-TEST
if st.button("🚀 Test-Datei speichern"):
    try:
        repo = g.get_repo("plankton31012010-cell/SilasGuardianPro")
        repo.create_file("test.txt", "Debug Test", "Es funktioniert!", branch="main")
        st.balloons()
        st.success("Datei wurde auf GitHub erstellt!")
    except Exception as e:
        st.error(f"Speichern fehlgeschlagen: {e}")
