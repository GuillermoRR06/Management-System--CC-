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
if len(appData["Eventos"]) == 0:
    for i in range(31):
        appData["Eventos"].append({ "id" : (dt.date.today() + dt.timedelta(i)).strftime('%B, %d, %Y'), "List_Events" : [], "In_Time" : True})
else:
    for e in appData["Eventos"]:
        if e["id"] != dt.date.today().strftime('%B, %d, %Y'):
            e["In_Time"] == False
        else: break
    for i in range(31):
        dy = (dt.date.today() + dt.timedelta(i)).strftime('%B, %d, %Y')
        is_in = False
        for e in appData["Eventos"]:
            if e["id"] == dy:
                is_in = True
                break
        if not is_in:
            appData["Eventos"].append({ "id" : dy, "List_Events" : [], "In_Time" : True})
        
Save_Data.SaveData(appData)
#-----------------------------------------------------------------------------------------------------------
st.session_state["Recursos"] = appData["Recursos"]
st.session_state["Eventos"] = appData["Eventos"]
#-----------------------------------------------------------------------------------------------------------
st.markdown("# Gestor de Eventos del Centro Cultural *La Casa de Papel*")
st.markdown("---")