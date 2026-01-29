import streamlit as st
from datetime import *
from Functions import RevisarRecursos
#-----------------------------------------------------------------------------------------------------------
res = st.session_state["Recursos"]
evens = st.session_state["Eventos"]
salas = res["salas"]
#-----------------------------------------------------------------------------------------------------------
def FindNewHour(hour: time, day: date):
    pass
#-----------------------------------------------------------------------------------------------------------
def FindNewDay(day: date) -> list:
    pass
        
#-----------------------------------------------------------------------------------------------------------
def FindTimeFree(hour: time, day: date):
    pass