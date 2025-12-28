import os
import time
import streamlit as st
import json
#-----------------------------------------------------------------------------------------------------------
@st.cache_data
def GetData(timestamp) -> dict:
    with open("Data\data.json", "r") as Data:
        appData = json.load(Data)
    return appData

def Get_Timestamp():
    return os.path.getmtime("Data\data.json")

def SaveData(data):
    with open("Data\data.json", "w") as Data:
        json.dump(data, Data, indent=4, ensure_ascii=True)