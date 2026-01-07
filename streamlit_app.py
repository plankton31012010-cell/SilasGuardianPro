import streamlit as st
from github import Github

# 1. Verbindung zu GitHub herstellen
def get_repo():
    try:
        token = st.secrets["GITHUB_TOKEN"]
        g = Github(token)
        return g.get_repo("plankton31012010-cell/SilasGuardianPro")
    except:
        return None

st.title("🛡️ SilasGuardian Safe")

# 2. Login Abfrage
if "login" not in st.session_state: st.session_state.login = False

if not st.session_state.login:
    pw = st.text_input("Master-Key", type="password")
    if st.button("Einloggen"):
        if pw == "silas":
            st.session_state.login = True
            st.rerun()
else:
    # 3. Sektor 3 Schreibbereich
    st.subheader("📁 Sektor 3: Dein Datentresor")
    repo = get_repo()
    
    if repo:
        st.success("✅ Verbindung zu GitHub steht!")
        
        # Versuchen, alte Notizen zu laden
        try:
            file = repo.get_contents("notizen.txt", ref="main")
            inhalt = file.decoded_content.decode()
        except:
            inhalt = "Schreibe hier deine ersten Notizen rein..."

        neuer_inhalt = st.text_area("Notizen:", value=inhalt, height=200)

        if st.button("💾 Jetzt auf GitHub speichern"):
            try:
                try:
                    # Update
                    old_file = repo.get_contents("notizen.txt", ref="main")
                    repo.update_file("notizen.txt", "Update", neuer_inhalt, old_file.sha, branch="main")
                except:
                    # Neu erstellen
                    repo.create_file("notizen.txt", "Erster Start", neuer_inhalt, branch="main")
                st.balloons()
                st.success("Gespeichert! Schau jetzt mal in dein GitHub-Profil.")
            except Exception as e:
                st.error(f"Fehler beim Speichern: {e}")
    else:
        st.error("❌ Fehler: Der GITHUB_TOKEN in den Secrets ist nicht korrekt.")
