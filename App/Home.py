import streamlit as st
import json
import datetime as dt
from Functions import Save_Data
#-----------------------------------------------------------------------------------------------------------
if "Recursos" not in st.session_state or "Events" not in st.session_state:
    appData = Save_Data.GetData()
#-----------------------------------------------------------------------------------------------------------
st.set_page_config(layout="wide")
#-----------------------------------------------------------------------------------------------------------
today = dt.date.today()
for e in appData["Eventos"]:
    d = dt.date(e["id"][0], e["id"][1], e["id"][2])
    if d < today:
        e["In_Time"] = False
    else: break
    
if len(appData["Eventos"]) >= 40:
    for e in appData["Eventos"]:
        if not e["In_Time"]:
            appData["Eventos"].remove(e)
Save_Data.SaveData(appData)
#-----------------------------------------------------------------------------------------------------------
st.session_state["Recursos"] = appData["Recursos"]
st.session_state["Eventos"] = appData["Eventos"]
#-----------------------------------------------------------------------------------------------------------
st.markdown("# Gestor de Eventos del Centro Cultural *La Cuarta Pared*")
st.markdown("---")