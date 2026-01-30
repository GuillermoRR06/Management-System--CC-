import streamlit as st
from datetime import *
from Functions import RevisarRecursos
#-----------------------------------------------------------------------------------------------------------
evens = st.session_state["Eventos"]
#-----------------------------------------------------------------------------------------------------------
def FindNewHour_Place(evs: list, d: date, InitH: time, EndH: time, id: int):
    duration = EndH - InitH
    i = 7
    newInH = time(i, 50, 0)
    
    while i < InitH.hour:
        for t in range(5):
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
                st.success(f"Te recomiendo este nuevo horario para agregar el evento: {newInH.strftime('%H:%M')}")
                return
        i += 1
    
    i += 1 + duration.hour
    while i < 24:
        for t in range(5):
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
                st.success(f"Te recomiendo este nuevo horario para agregar el evento: {newInH.strftime('%H:%M')}")
                return
        i += 1
        
    FindNewDay(d) 
    return null 
#-----------------------------------------------------------------------------------------------------------
def FindNewDay(day: date):
    st.success("Hoy no es el mejor dia para programar este evento. Prueba con estos dias")
    l = 0
    for i in range(1, 31):
        newD = day + timedelta(i)
        j = RevisarRecursos.BS_Date(evens, newD)
        if len(evens[j]) < 6:
            l += 1
            st.success(newD.strftime('%B, %d, %Y'))
            if l == 3: return l
#-----------------------------------------------------------------------------------------------------------