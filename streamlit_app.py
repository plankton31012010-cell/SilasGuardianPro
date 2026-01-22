import streamlit as st
import os, time, datetime, random
try:
    import plotly.express as px
    PLOTLY = True
except:
    PLOTLY = False

st.set_page_config(page_title="SilasGuardian", layout="wide")
VP = "sector_3_vault"
LOG = os.path.join(VP, "log.txt")
BR = os.path.join(VP, "bridge.txt")
if not os.path.exists(VP): os.makedirs(VP)
HOME = {"lat": 52.9126, "lon": 8.8217}

if 'auth' not in st.session_state: st.session_state.update({'auth': "A0", 'time': None, 'scan': False, 'vault': False, 'crash': False})

def reset():
    st.session_state.update({'auth': "A0", 'time': None, 'scan': False, 'vault': False, 'crash': False})
    st.rerun()

st.markdown("<style>.stApp{background-color:#050505;color:#00ff41;font-family:monospace;}</style>", unsafe_allow_html=True)

if st.session_state.crash:
    st.title("☣️ CRASH")
    if st.button("REBOOT"): reset()
    st.stop()

if st.session_state.auth == "A0":
    st.title("🛡️ Login")
    id_in = st.text_input("Ident", type="password")
    pw_in = st.text_input("Sektor-Passwort", type="password")
    if st.button("Boot"):
        if id_in.lower() == "silas" and pw_in.lower() == "data":
            st.session_state.auth = "A1+"
            st.session_state.time = time.time()
            st.rerun()
    st.stop()

if (time.time() - st.session_state.time) < 3:
    st.title("Willkommen Anton")
    time.sleep(1); st.rerun()

t1, t2, t3, t4 = st.tabs(["🌍 Map", "📡 Scan", "📂 Vault", "🛡️ Zero"])

with t1:
    if PLOTLY:
        d = []
        for _ in range(10):
            d.append({'lat':random.uniform(-30,60),'lon':random.uniform(-100,120),'Info':'THREAT','S':random.randint(10,30),'C':'G'})
        d.append({'lat':HOME['lat'],'lon':HOME['lon'],'Info':'HOME (SYKE)','S':50,'C':'R'})
        df = pd.DataFrame(d)
        fig = px.scatter_geo(df,lat='lat',lon='lon',size='S',color='C',color_discrete_map={'G':'#00ff41','R':'#ff0000'})
        fig.update_layout(template="plotly_dark", margin=dict(l=0,r=0,t=0,b=0), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    else: st.error("Lade Map...")

with t2:
    if st.button("Start Scan"):
        p = st.progress(0)
        for i in range(100): time.sleep(0.01); p.progress(i+1)
        st.session_state.scan = True
    if st.session_state.scan: st.success("Netzwerk sicher.")

with t3:
    if st.session_state.vault:
        st.error("VAULT PURGED")
        if st.button("Restore"): st.session_state.vault = False; st.rerun()
    else:
        if st.button("🧨 SELBSTZERSTÖRUNG"): st.session_state.vault = True; st.rerun()
        up = st.file_uploader("Upload")
        if up: 
            with open(os.path.join(VP, up.name),"wb") as f: f.write(up.getbuffer())
        for fn in os.listdir(VP):
            if fn not in ["log.txt", "bridge.txt"]:
                with open(os.path.join(VP, fn), "rb") as fb: st.download_button(f"🔓 {fn}", fb, file_name=fn)

with t4:
    if st.toggle("PANIC"): st.session_state.crash = True; st.rerun()
    if st.button("OFF"): reset()
