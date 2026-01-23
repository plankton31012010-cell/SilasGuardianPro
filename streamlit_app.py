import streamlit as st
import os, time, datetime, random
import pandas as pd

# Plotly Check
try:
    import plotly.express as px
    MAP_ON = True
except:
    MAP_ON = False

# Setup
st.set_page_config(page_title="SilasGuardian", layout="wide")
VP = "sector_3_vault"
if not os.path.exists(VP): os.makedirs(VP)
HOME = {"lat": 52.9126, "lon": 8.8217}

# Session State
if 'auth' not in st.session_state:
    st.session_state.update({'auth':"A0",'t':0,'v':False,'c':False})

# Styling
st.markdown("<style>.stApp{background-color:#050505;color:#00ff41;font-family:monospace;}</style>",unsafe_allow_html=True)

# Crash Check
if st.session_state.c:
    st.title("☣️ SYSTEM HALTED")
    if st.button("REBOOT"):
        st.session_state.update({'auth':"A0",'c':False})
        st.rerun()
    st.stop()

# Login
if st.session_state.auth == "A0":
    st.title("🛡️ SilasGuardian Login")
    u = st.text_input("Ident", type="password")
    p = st.text_input("Sektor-Passwort", type="password")
    if st.button("Boot"):
        if u.lower() == "silas" and p.lower() == "data":
            st.session_state.auth = "A1"
            st.session_state.t = time.time()
            st.rerun()
    st.stop()

# Dashboard
t1, t2, t3, t4 = st.tabs(["🌍 Map", "📡 Scan", "📂 Vault", "🛡️ Zero"])

with t1:
    if MAP_ON:
        st.subheader("Globale Bedrohungen")
        pts = []
        for _ in range(10):
            pts.append({'lat':random.uniform(-30,60),'lon':random.uniform(-100,120),'Info':'Attack','S':20,'C':'G'})
        pts.append({'lat':HOME['lat'],'lon':HOME['lon'],'Info':'HOMEBASE','S':50,'C':'R'})
        df = pd.DataFrame(pts)
        fig = px.scatter_geo(df,lat='lat',lon='lon',size='S',color='C',color_discrete_map={'G':'#00ff41','R':'#ff0000'})
        fig.update_layout(template="plotly_dark",margin=dict(l=0,r=0,t=0,b=0),showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Installiere Plotly...")

with t2:
    if st.button("Deep Scan"):
        bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            bar.progress(i+1)
        st.success("Netzwerk Scan abgeschlossen.")

with t3:
    if st.session_state.v:
        st.error("⚠️ VAULT GELÖSCHT (FAKE)")
        if st.button("Reset"):
            st.session_state.v = False
            st.rerun()
    else:
        if st.button("🧨 SELBSTZERSTÖRUNG"):
            st.session_state.v = True
            st.rerun()
        st.divider()
        for fn in os.listdir(VP):
            with open(os.path.join(VP, fn), "rb") as f:
                st.download_button(f"🔓 {fn}", f, file_name=fn)

with t4:
    if st.toggle("PANIC MODE"):
        st.session_state.c = True
        st.rerun()
    if st.button("OFF"):
        st.session_state.auth = "A0"
        st.rerun()
