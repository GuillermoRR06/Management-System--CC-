import streamlit as st
from datetime import *
from Functions import RevResources, AuxFuncs
#-----------------------------------------------------------------------------------------------------------
evens = st.session_state["Eventos"]
#-----------------------------------------------------------------------------------------------------------
def FindNewHour_Film_Theather(evs: list, d: date, InitH: time, EndH: time, tip: str, id: int, emplsNed: dict):
    if EndH.hour >= InitH.hour: duration = (EndH.hour - InitH.hour, EndH.minute - InitH.minute)
    else:
        FindNewDay(d) 
        return
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
                if hr > 23: hr = hr % 24
            newEnH = time(hour=hr, minute=mint)
            res = RevResources.Disponibility(evs, d, newInH, newEnH)
            NotMC = RevResources.Check_MC(evs, d, newInH, newEnH, False)
            NotAllPls = RevResources.Check_Places(res["salas"], False)
            NotAllPers = RevResources.Check_Personal(res, tip, False)
            YesPlace = RevResources.Review_Place(id, res["salas"], False)
            YesPersonal = RevResources.Review_Personal(res, emplsNed, False)
            if NotMC and NotAllPls and NotAllPers and YesPlace and YesPersonal:
                st.success(f"Te recomiendo este nuevo horario para agregar el evento: {newInH.strftime('%H:%M')}")
                return
        i += 1
    
    i += 1 + duration[0]
    if i > 23:
        FindNewDay(d) 
        return
    newInH = time(i, 50, 0)
    while i < 24:
        for t in range(5):
            hr = newInH.hour
            mint = newInH.minute + 10
            if mint >= 60:
                mint = mint % 60
                hr += 1
                if hr > 23:
                    FindNewDay(d) 
                    return
            newInH = time(hour=hr, minute=mint)
            hr = newInH.hour + duration[0]
            if hr > 23: hr = hr % 24
            mint = newInH.minute + duration[1]
            if mint >= 60:
                mint = mint % 60
                hr += 1
                if hr > 23:
                    FindNewDay(d) 
                    return
            newEnH = time(hour=hr, minute=mint)
            res = RevResources.Disponibility(evs, d, newInH, newEnH)
            NotMC = RevResources.Check_MC(evs, d, newInH, newEnH, False)
            NotAllPls = RevResources.Check_Places(res["salas"], False)
            NotAllPers = RevResources.Check_Personal(res, tip, False)
            YesPlace = RevResources.Review_Place(id, res["salas"], False)
            YesPersonal = RevResources.Review_Personal(res, emplsNed, False)
            if NotMC and NotAllPls and NotAllPers and YesPlace and YesPersonal:
                st.success(f"Te recomiendo este nuevo horario para agregar el evento: {newInH.strftime('%H:%M')}")
                return
        i += 1
        
    FindNewDay(d) 
    return
#-----------------------------------------------------------------------------------------------------------
def FindNewHour_Music(evs: list, d: date, InitH: time, EndH: time):
    if EndH.hour >= InitH.hour: duration = (EndH.hour - InitH.hour, EndH.minute - InitH.minute)
    else:
        FindNewDay(d) 
        return
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
            res = RevResources.Disponibility(evs, d, newInH, newEnH)
            NotOEvs = RevResources.Check_Evs(evs, d, newInH, newEnH, False)
            if NotOEvs:
                st.success(f"Te recomiendo este nuevo horario para agregar el evento: {newInH.strftime('%H:%M')}")
                return
        i += 1
    
    i += 1 + duration[0]
    if i > 23:
        FindNewDay(d) 
        return
    newInH = time(i, 50, 0)
    while i < 24:
        for t in range(5):
            hr = newInH.hour
            mint = newInH.minute + 10
            if mint >= 60:
                mint = mint % 60
                hr += 1
                if hr > 23:
                    FindNewDay(d) 
                    return
            newInH = time(hour=hr, minute=mint)
            hr = newInH.hour + duration[0]
            if hr > 23: hr = hr % 24
            mint = newInH.minute + duration[1]
            if mint >= 60:
                mint = mint % 60
                hr += 1
                if hr > 23:
                    FindNewDay(d) 
                    return
            newEnH = time(hour=hr, minute=mint)
            res = RevResources.Disponibility(evs, d, newInH, newEnH)
            NotOEvs = RevResources.Check_Evs(evs, d, newInH, newEnH, False)
            if NotOEvs:
                st.success(f"Te recomiendo este nuevo horario para agregar el evento: {newInH.strftime('%H:%M')}")
                return
        i += 1
    FindNewDay(d) 
    return
#-----------------------------------------------------------------------------------------------------------
def FindNewDay(day: date):
    st.success("Hoy no es el mejor dia para programar este evento. Prueba con estos dias")
    l = 0
    for i in range(1, 31):
        newD = day + timedelta(i)
        j = AuxFuncs.BS_Date(evens, newD)
        if len(evens[j]) < 6:
            l += 1
            st.success(newD.strftime('%B, %d, %Y'))
            if l == 3: return
    st.error("Ups, parece que los proximos 30 dias estan demasiado ocupados. Espera a manana para agregar un nuevo evento")
#-----------------------------------------------------------------------------------------------------------