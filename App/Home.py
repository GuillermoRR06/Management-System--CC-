import streamlit as st
import json
import datetime as dt
from Functions import Save_Data
#-----------------------------------------------------------------------------------------------------------
with open("Data\data.json", "r") as Data:
    appData = json.load(Data)
#-----------------------------------------------------------------------------------------------------------
st.set_page_config(layout="wide")
#-----------------------------------------------------------------------------------------------------------
today = dt.date.today()
for e in appData["Eventos"]:
    if e["id"] != (today.year, today.month, today.day):
        e["In_Time"] == False
    else: break   
Save_Data.SaveData(appData)
#-----------------------------------------------------------------------------------------------------------
st.session_state["Recursos"] = appData["Recursos"]
st.session_state["Eventos"] = appData["Eventos"]
#-----------------------------------------------------------------------------------------------------------
st.markdown("# Gestor de Eventos del Centro Cultural *La Casa de Papel*")
st.markdown("---")