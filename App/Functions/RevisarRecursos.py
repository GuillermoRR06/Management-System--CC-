import streamlit as st
from datetime import *

def Disponibility(events: list, day: date, tm: time) -> dict:
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
        if list(d.keys())[0] == day.strftime('%B, %d, %Y'):
            ev = d[day.strftime('%B, %d, %Y')]
            break
    
    for e in ev:
        hora_inicio = datetime.strptime(e["hora de inicio"], '%H:%M').time()
        hora_final = datetime.strptime(e["hora de fin"], '%H:%M').time()
        if hora_inicio <= tm or tm <= hora_final:
            dispons["personal de limpieza"] -= e["personal de limpieza"]
            dispons["tecnicos de sonido"] -= e["tecnicos de sonido"]
            dispons["tecnicos de iluminacion"] -= e["tecnicos de iluminacion"]
            dispons["operadores de proyeccion"] -= e["operadores de proyeccion"]
            dispons["personal de seguridad"] -= e["personal de seguridad"]
            dispons["salas"][e["sala"]-1] = False
    return dispons

def Review_Place(id: int, salas: list) -> bool:
    if not salas[id-1]:
        st.success(f"La sala #{id} no esta disponible en el horario escogido")
        return False
    else:
        return True

def Review_Capacity(sala: dict, assistance: int) -> bool:
    if sala["capacidad"] < assistance:
        st.success(f"La sala seleccionada no tiene suficientes butacas para {assistance} personas")
        return False
    return True

def Review_Filme(personal_disponible : dict, personal_necesario: dict) -> bool:
    ok = True
    for key in personal_disponible.keys():
        if key in personal_necesario.keys():
            if personal_necesario[key] > personal_disponible[key]:
                ok = False
                st.success(f"No se dispone de {personal_necesario[k]} {k} para la hora del evento")
    return ok

def AddEvent(events: list, typ: str, day: date, tm_Init: time, tm_End: time, name: str, recursos: dict) -> None:
    newEvent = {
        "nombre": name,
        "tipo": typ.capitalize(),
        "fecha": day.strftime('%B, %d, %Y'),
        "hora de inicio": tm_Init.strftime('%H:%M'),
        "hora de fin": tm_End.strftime('%H:%M')
    }
    newEvent.update(recursos)
    
    ev = []
    for d in events:
        if list(d.keys())[0] == day.strftime('%B, %d, %Y'):
            ev = d[day.strftime('%B, %d, %Y')]
            break
    
    if len(ev) == 0:
        ev.append(newEvent)
    else:
        index = len(ev)-1
        for i in range(len(ev)):
            hora = datetime.strptime(ev[i]["hora de inicio"], '%H:%M').time()
            if hora <= tm_Init:
                index = i
                break
        ev.insert(index, newEvent)