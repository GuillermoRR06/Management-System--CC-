import streamlit as st
from datetime import *
from Functions import RevisarRecursos
#-----------------------------------------------------------------------------------------------------------
evens = st.session_state["Eventos"]
#-----------------------------------------------------------------------------------------------------------
def FindNewHour_Film_Theather(evs: list, d: date, InitH: time, EndH: time, tip: str, id: int, emplsNed: dict):
    duration = (EndH.hour - InitH.hour, EndH.minute - InitH.minute)
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
            hr = newInH.hour + duration[0]
            mint = newInH.minute + duration[1]
            if mint >= 60:
                mint = mint % 60
                hr += 1
            newEnH = time(hour=hr, minute=mint)
            res = RevisarRecursos.Disponibility(evs, d, newInH, newEnH)
            NotMC = RevisarRecursos.Check_MC(evs, d, newInH, newEnH, False)
            NotAllPls = RevisarRecursos.Check_Places(res["salas"], False)
            NotAllPers = RevisarRecursos.Check_Personal(res, tip, False)
            YesPlace = RevisarRecursos.Review_Place(id, res["salas"], False)
            YesPersonal = RevisarRecursos.Review_Personal(res, emplsNed, False)
            if NotMC and NotAllPls and NotAllPers and YesPlace and YesPersonal:
                st.success(f"Te recomiendo este nuevo horario para agregar el evento: {newInH.strftime('%H:%M')}")
                return
        i += 1
    
    i += 1 + duration[0]
    newInH = time(i, 50, 0)
    while i < 24:
        for t in range(5):
            hr = newInH.hour
            mint = newInH.minute + 10
            if mint >= 60:
                mint = mint % 60
                hr += 1
            newInH = time(hour=hr, minute=mint)
            res = RevisarRecursos.Disponibility(evs, d, newInH, newEnH)
            NotMC = RevisarRecursos.Check_MC(evs, d, newInH, newEnH, False)
            NotAllPls = RevisarRecursos.Check_Places(res["salas"], False)
            NotAllPers = RevisarRecursos.Check_Personal(res, tip, False)
            YesPlace = RevisarRecursos.Review_Place(id, res["salas"], False)
            YesPersonal = RevisarRecursos.Review_Personal(res, emplsNed, False)
            if NotMC and NotAllPls and NotAllPers and YesPlace and YesPersonal:
                st.success(f"Te recomiendo este nuevo horario para agregar el evento: {newInH.strftime('%H:%M')}")
                return
        i += 1
        
    FindNewDay(d) 
    return
#-----------------------------------------------------------------------------------------------------------
def FindNewHour_Music(evs: list, d: date, InitH: time, EndH: time):
    duration = (EndH.hour - InitH.hour, EndH.minute - InitH.minute)
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
            hr = newInH.hour + duration[0]
            mint = newInH.minute + duration[1]
            if mint >= 60:
                mint = mint % 60
                hr += 1
            newEnH = time(hour=hr, minute=mint)
            res = RevisarRecursos.Disponibility(evs, d, newInH, newEnH)
            NotOEvs = RevisarRecursos.Check_Evs(evs, d, newInH, newEnH, False)
            if NotOEvs:
                st.success(f"Te recomiendo este nuevo horario para agregar el evento: {newInH.strftime('%H:%M')}")
                return
        i += 1
    
    i += 1 + duration[0]
    newInH = time(i, 50, 0)
    while i < 24:
        for t in range(5):
            hr = newInH.hour
            mint = newInH.minute + 10
            if mint >= 60:
                mint = mint % 60
                hr += 1
            newInH = time(hour=hr, minute=mint)
            print(newInH)
            res = RevisarRecursos.Disponibility(evs, d, newInH, newEnH)
            NotOEvs = RevisarRecursos.Check_Evs(evs, d, newInH, newEnH, False)
            print(NotOEvs)
            if NotOEvs:
                st.success(f"Te recomiendo este nuevo horario para agregar el evento: {newInH.strftime('%H:%M')}")
                return
        i += 1
    print(i)
    FindNewDay(d) 
    return
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
            if l == 3: return
    st.error("Ups, parece que los proximos 30 dias estan demasiado ocupados. Espera a manana para agregar un nuevo evento")
#-----------------------------------------------------------------------------------------------------------