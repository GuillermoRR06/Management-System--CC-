import streamlit as st
from datetime import *
from Functions import Save_Data
from Functions import AuxFuncs
#-----------------------------------------------------------------------------------------------------------
res = st.session_state["Recursos"]
evens = st.session_state["Eventos"]
#-----------------------------------------------------------------------------------------------------------
# Funciones que permiten analizar el choque de recursos
def Review_Events(events: list) -> bool:
    for e in events:
        if e["activo"]: return True
    return False
#-----------------------------------------------------------------------------------------------------------
def Disponibility(events: list, day: date, tm_Inicial: time, tm_Final: time) -> dict:
    '''
    Analiza la disponibilidad de los recursos del cine-teatro en la hora escogida
    Retorna un diccionario con los recursos disponibles en el momento escogido
    '''
    dispons = {
        "personal de limpieza": 8,
        "tecnicos de sonido": 6,
        "tecnicos de iluminacion": 6,
        "operadores de proyeccion": 6,
        "personal de seguridad": 8,
        "salas": [True, True, True, True, True, True]
    }
    
    ev = []
    for d in events:
        if date(d["id"][0], d["id"][1], d["id"][2]) == date(day.year, day.month, day.day):
            ev = d["Lista_Eventos"]

    for e in ev:
        if e["activo"]:
            hora_inicio = datetime.strptime(e["hora de inicio"], '%H:%M').time()
            hora_final = datetime.strptime(e["hora de fin"], '%H:%M').time()
            if (hora_inicio <= tm_Inicial and tm_Inicial <= hora_final) or (hora_inicio <= tm_Final and tm_Final <= hora_final) or (tm_Inicial <= hora_inicio and hora_final <= tm_Final):
                dispons["personal de seguridad"] -= e["personal de seguridad"]
                dispons["tecnicos de sonido"] -= e["tecnicos de sonido"]
                if "tecnicos de iluminacion" in e.keys():
                    dispons["tecnicos de iluminacion"] -= e["tecnicos de iluminacion"]
                if "operadores de proyeccion" in e.keys():
                    dispons["operadores de proyeccion"] -= e["operadores de proyeccion"]
            hr = hora_final.hour
            mint = hora_final.minute + 30
            if mint >= 60:
                mint = mint % 60
                hr += 1
            hora_final = time(hour=hr, minute=mint)
            if (hora_inicio <= tm_Inicial and tm_Inicial <= hora_final) or (hora_inicio <= tm_Final and tm_Final <= hora_final) or (tm_Inicial <= hora_inicio and hora_final <= tm_Final):
                dispons["personal de limpieza"] -= e["personal de limpieza"]
                dispons["salas"][e["sala"]-1] = False
    return dispons
#-----------------------------------------------------------------------------------------------------------
def Check_Places(salas: list, k: bool) -> bool:
    '''
    Revisa si todas las salas estan disponibles en el momento
    '''
    ok = True
    if ok not in salas:
        if k: st.error("❌ No hay salas disponibles en este horario")
        return False
    return True
#-----------------------------------------------------------------------------------------------------------
def Check_Personal(res: dict, typ: str, k: bool) -> bool:
    '''
    Revisa si el personal esta disponible
    '''
    ok = True
    if res["personal de limpieza"] == 0:
        if k: st.error("❌ No hay personal de limpieza disponible en este horario")
        ok = False
    elif res["personal de seguridad"] == 0:
        if k: st.error("❌ No hay personal de seguridad disponible en este horario")
        ok = False
    elif res["tecnicos de sonido"] == 0:
        if k: st.error("❌ No hay tecnicos de sonido disponibles en este horario")
        ok = False
    else:
        if typ == "Proyeccion Filmica":
            if res["operadores de proyeccion"] == 0:
                if k: st.error("❌ No hay operadores de proyeccion disponibles en este horario")
                ok = False
        else:
            if res["tecnicos de iluminacion"] == 0:
                if k: st.error("❌ No hay tecnicos de iluminacion disponibles en este horario")
                ok = False
    return ok
#-----------------------------------------------------------------------------------------------------------
def Check_MC(events: list, day: date, tm1: time, tm2: time, k: bool) -> bool:
    '''
    Revisa si hay un concierto musical en el horario seleccionado
    '''
    d = AuxFuncs.BS_Date(events, day)
    if d != -1:
        for e in events[d]["Lista_Eventos"]:
            if e["activo"] and e["tipo"] == "Concierto Musical":
                h1 = datetime.strptime(e["hora de inicio"], '%H:%M').time()
                h2 = datetime.strptime(e["hora de fin"], '%H:%M').time()
                hr = h2.hour
                mint = h2.minute + 30
                if mint >= 60:
                    mint = mint % 60
                    hr += 1
                h2 = time(hour=hr, minute=mint)
                if (h1 <= tm1 and tm1 <= h2) or (h1 <= tm2 and tm2 <= h2) or (tm1 <= h1 and h2 <= tm2):
                    if k: st.error("❌ No es posible programar eventos en este horario. Hay un concierto musical")
                    return False
    return True  
#-----------------------------------------------------------------------------------------------------------
def Check_Evs(events: list, day: date, tm1: time, tm2: time, k: bool) -> bool:
    '''
    Revisa si es posible programar un concierto musical en un determiando horario (no puede coincidir con otros eventos)
    '''
    d = AuxFuncs.BS_Date(events, day)
    if d != -1:
        for e in events[d]["Lista_Eventos"]:
            if e["activo"]:
                h1 = datetime.strptime(e["hora de inicio"], '%H:%M').time()
                haux = datetime.strptime(e["hora de fin"], '%H:%M').time()
                hr = haux.hour
                mint = haux.minute + 30
                if mint >= 60:
                    mint = mint % 60
                    hr += 1
                h2 = time(hour=hr, minute=mint)
                if (h1 <= tm1 and tm1 <= h2) or (h1 <= tm2 and tm2 <= h2) or (tm1 <= h1 and h2 <= tm2):
                    if k: st.error("❌ No es posible programar un concierto musical en este horario. Ya hay otros eventos")
                    return False
    return True
#-----------------------------------------------------------------------------------------------------------
def Review_Place(id: int, salas: list, k: bool) -> bool:
    '''
    Analiza si la sala escogida se encuentra disponible en el horario establecido
    '''
    if not salas[id]:
        if k: st.error(f"❌ La sala #{id+1} no esta disponible en el horario escogido")
        return False
    else:
        return True
#-----------------------------------------------------------------------------------------------------------
def Review_Capacity(sala: dict, assistance: int, k: bool) -> bool:
    '''
    Analiza si la sala escogida tiene capacidad suficiente para la cantidad de asistentes
    '''
    if sala["capacidad"] < assistance:
        if k: st.error(f"❌ La sala seleccionada no tiene suficientes butacas para {assistance} personas")
        return False
    return True
#-----------------------------------------------------------------------------------------------------------
def Review_PersCapacity(persL: int, persS: int, assistance: int, k: bool) -> bool:
    '''
    Analiza si la cantidad de personal seleccionado esta acorde a la asistencia del publico
    '''
    ok = True
    cap = 1 if assistance < 100 else 2 if assistance < 200 else 3
    
    if persL < cap:
        if k: st.error(f"❌ La asistencia al evento es de {assistance} personas, por tanto necesitas al menos {cap} personas de limpieza")
        ok = False
    if persS < cap:
        if k: st.error(f"❌ La asistencia al evento es de {assistance} personas, por tanto necesitas al menos {cap} personas de seguridad")
        ok = False
        
    return ok
#-----------------------------------------------------------------------------------------------------------
def Review_PersPlace(persS: int, persP: int, persL: int, id: int, k: bool):
    '''
    Analiza si la cantidad de personal seleccionado esta acorde a la sala del evento
    '''
    ok = True
    if id in [4, 5]:
        if persS < 2:
            if k: st.error(f"❌ La sala {id} necesita al menos 2 tecnicos de sonido")
            ok = False
        if persP != 0 and persP < 2:
            if k: st.error(f"❌ La sala {id} necesita al menos 2 operadores de proyeccion")
            ok = False
        if persL != 0 and persL < 2:
            if k: st.error(f"❌ La sala {id} necesita al menos 2 tecnicos de iluminacion")
            ok = False
            
    elif id == 6:
        if persS < 3:
            if k: st.error(f"❌ La sala {id} necesita al menos 3 tecnicos de sonido")
            ok = False
        if persP != 0 and persP < 3:
            if k: st.error(f"❌ La sala {id} necesita al menos 3 operadores de proyeccion")
            ok = False
        if persL != 0 and persL < 3:
            if k: st.error(f"❌ La sala {id} necesita al menos 3 tecnicos de iluminacion")
            ok = False
            
    return ok
#-----------------------------------------------------------------------------------------------------------
def Review_Scene(id: int, k: bool) -> bool:
    '''
    Analiza si la sala escogida posee un escenario modular (estas son: #4, #5, #6)
    '''
    if id in [0, 1, 2]:
        if k: st.error(f"❌ La sala #{id+1} no posee un escenario modular.")
        return False
    else:
        return True
#-----------------------------------------------------------------------------------------------------------
def Review_Personal(personal_disponible : dict, personal_necesario: dict, k: bool) -> bool:
    '''
    Analiza, a partir del personal disponible y el personal necesario, si es posible efectuar el evento
    '''
    ok = True
    for key in personal_disponible.keys():
        if key in personal_necesario.keys():
            if personal_necesario[key] > personal_disponible[key]:
                ok = False
                if k: st.error(f"❌ No se dispone de {personal_necesario[key]} {key} para la hora del evento")
    return ok
#-----------------------------------------------------------------------------------------------------------