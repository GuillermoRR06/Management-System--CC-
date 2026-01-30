import streamlit as st
from datetime import *
from Functions import RevisarRecursos
#-----------------------------------------------------------------------------------------------------------
evens = st.session_state["Eventos"]
#-----------------------------------------------------------------------------------------------------------
def FindNewHour_Place(evs: list, d: date, InitH: time, EndH: time, id: int) -> time:
    duration = EndH - InitH
    i = 7
    newInH = time(i, 50, 0)
    
    while i < InitH.hour:
        for i in range(5):
            hr = newInH.hour
            mint = newInH.minute + 10
            if mint >= 60:
                mint = mint % 60
                hr += 1
            newInH = time(hour=hr, minute=mint)
            newEnH = newInH + duration
            res = RevisarRecursos.Disponibility(evs, d, newInH, newEnH)
            s = res["salas"]
            if s[id]:
                return newInH
        i += 1
    
    i += 1 + duration.hour + (duration.minute//60)
    while i < 24:
        for i in range(0, 60, step=10):
            newInH += timedelta(minutes=i)
            newEnH = newInH + duration
            res = RevisarRecursos.Disponibility(evs, d, newInH, newEnH)
            s = res["salas"]
            if s[id]:
                return newInH
        i += 1
        
    st.success("Hoy no es el mejor dia para programar este evento. Prueba con estos dias")
    ld = FindNewDay(d)
    for e in ld: st.success(e.strftime('%B, %d, %Y'))
    return null 
#-----------------------------------------------------------------------------------------------------------
def FindNewDay(day: date) -> list:
    l = []
    for i in range(30):
        newD = day + timedelta(i)
        if len(eve)