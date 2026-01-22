import streamlit as st
from datetime import *
from Functions import Save_Data
#-----------------------------------------------------------------------------------------------------------
res = st.session_state["Recursos"]
evens = st.session_state["Eventos"]
#-----------------------------------------------------------------------------------------------------------
# Funciones que permiten analizar el choque de recursos
def Review_Events(events: list) -> bool:
    for e in events:
        if e["activo"]: return True
    return False

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
                dispons["personal de limpieza"] -= e["personal de limpieza"]
                dispons["personal de seguridad"] -= e["personal de seguridad"]
                dispons["salas"][e["sala"]-1] = False
                dispons["tecnicos de sonido"] -= e["tecnicos de sonido"]
                if "tecnicos de iluminacion" in e.keys():
                    dispons["tecnicos de iluminacion"] -= e["tecnicos de iluminacion"]
                if "operadores de proyeccion" in e.keys():
                    dispons["operadores de proyeccion"] -= e["operadores de proyeccion"]
    return dispons

def Check_Places(salas: list) -> bool:
    '''
    Revisa si todas las salas estan disponibles en el momento
    '''
    ok = True
    if ok not in salas:
        st.success("❌ No hay salas disponibles en este horario")
        return False
    return True

def Check_Personal(res: dict, typ: str) -> bool:
    '''
    Revisa si el personal esta disponible
    '''
    ok = True
    if res["personal de limpieza"] == 0:
        st.success("❌ No hay personal de limpieza disponible en este horario")
        ok = False
    elif res["personal de seguridad"] == 0:
        st.success("❌ No hay personal de seguridad disponible en este horario")
        ok = False
    elif res["tecnicos de sonido"] == 0:
        st.success("❌ No hay tecnicos de sonido disponibles en este horario")
        ok = False
    else:
        if typ == "Proyeccion Filmica":
            if res["operadores de proyeccion"] == 0:
                st.success("❌ No hay operadores de proyeccion disponibles en este horario")
                ok = False
        else:
            if res["tecnicos de iluminacion"] == 0:
                st.success("❌ No hay tecnicos de iluminacion disponibles en este horario")
                ok = False
    return ok

def Check_MC(events: list, day: date, tm1: time, tm2: time) -> bool:
    '''
    Revisa si hay un concierto musical en el horario seleccionado
    '''
    d = BS_Date(events, day)
    if d != -1:
        for e in events[d]["Lista_Eventos"]:
            if e["activo"] and e["tipo"] == "Concierto Musical":
                h1 = datetime.strptime(e["hora de inicio"], '%H:%M').time()
                h2 = datetime.strptime(e["hora de fin"], '%H:%M').time()
                if (tm1 >= h1 and tm1 <= h2) or (tm2 >= h1 and tm2 <= h2) or (h1 <= tm1 and h2 <= tm2):
                    st.success("❌ No es posible programar eventos en este horario. Hay un concierto musical")
                    return False
    return True  

def Check_Evs(events: list, day: date, tm1: time, tm2: time) -> bool:
    '''
    Revisa si es posible programar un concierto musical en un determiando horario (no puede coincidir con otros eventos)
    '''
    d = BS_Date(events, day)
    if d != -1:
        for e in events[d]["Lista_Eventos"]:
            if e["activo"]:
                h1 = datetime.strptime(e["hora de inicio"], '%H:%M').time()
                h2 = datetime.strptime(e["hora de fin"], '%H:%M').time()
                if (tm1 >= h1 and tm1 <= h2) or (tm2 >= h1 and tm2 <= h2):
                    st.success("❌ No es posible programar un concierto musical en este horario. Ya hay otros eventos")
                    return False
    return True

def Review_Place(id: int, salas: list) -> bool:
    '''
    Analiza si la sala escogida se encuentra disponible en el horario establecido
    '''
    if not salas[id]:
        st.success(f"❌ La sala #{id+1} no esta disponible en el horario escogido")
        return False
    else:
        return True

def Review_Capacity(sala: dict, assistance: int) -> bool:
    '''
    Analiza si la sala escogida tiene capacidad suficiente para la cantidad de asistentes
    '''
    if sala["capacidad"] < assistance:
        st.success(f"❌ La sala seleccionada no tiene suficientes butacas para {assistance} personas")
        return False
    return True

def Review_PersCapacity(persL: int, persS: int, assistance: int) -> bool:
    '''
    Analiza si la cantidad de personal seleccionado esta acorde a la asistencia del publico
    '''
    ok = True
    cap = 1 if assistance < 100 else 2 if assistance < 200 else 3
    
    if persL < cap:
        st.success(f"❌ La asistencia al evento es de {assistance} personas, por tanto necesitas al menos {cap} personas de limpieza")
        ok = False
    if persS < cap:
        st.success(f"❌ La asistencia al evento es de {assistance} personas, por tanto necesitas al menos {cap} personas de seguridad")
        ok = False
        
    return ok

def Review_PersPlace(persS: int, persP: int, persL: int, id: int):
    '''
    Analiza si la cantidad de personal seleccionado esta acorde a la sala del evento
    '''
    ok = True
    if id in [4, 5]:
        if persS < 2:
            st.success(f"❌ La sala {id} necesita al menos 2 tecnicos de sonido")
            ok = False
        if persP != 0 and persP < 2:
            st.success(f"❌ La sala {id} necesita al menos 2 operadores de proyeccion")
            ok = False
        if persL != 0 and persL < 2:
            st.success(f"❌ La sala {id} necesita al menos 2 tecnicos de iluminacion")
            ok = False
            
    elif id == 6:
        if persS < 3:
            st.success(f"❌ La sala {id} necesita al menos 3 tecnicos de sonido")
            ok = False
        if persP != 0 and persP < 3:
            st.success(f"❌ La sala {id} necesita al menos 3 operadores de proyeccion")
            ok = False
        if persL != 0 and persL < 3:
            st.success(f"❌ La sala {id} necesita al menos 3 tecnicos de iluminacion")
            ok = False
            
    return ok

def Review_Scene(id: int) -> bool:
    '''
    Analiza si la sala escogida posee un escenario modular (estas son: #4, #5, #6)
    '''
    if id in [0, 1, 2]:
        st.success(f"❌ La sala #{id+1} no posee un escenario modular.")
        return False
    else:
        return True

def Review_Personal(personal_disponible : dict, personal_necesario: dict) -> bool:
    '''
    Analiza, a partir del personal disponible y el personal necesario, si es posible efectuar el evento
    '''
    ok = True
    for key in personal_disponible.keys():
        if key in personal_necesario.keys():
            if personal_necesario[key] > personal_disponible[key]:
                ok = False
                st.success(f"❌ No se dispone de {personal_necesario[key]} {key} para la hora del evento")
    return ok
#-----------------------------------------------------------------------------------------------------------
# Funciones clave de la aplicacion: agregar, ver detalles y eliminar eventos
def AddEvent(events: list, typ: str, day: date, tm_Init: time, tm_End: time, name: str, description: str, recursos: dict) -> None:
    '''
    Agrega los eventos de forma que en un mismo dia todos queden ordenados cronologicamente
    '''
    newEvent = {
        "activo": True,
        "nombre": name,
        "tipo": typ,
        "descripcion": description,
        "fecha": day.strftime('%B, %d, %Y'),
        "hora de inicio": tm_Init.strftime('%H:%M'),
        "hora de fin": tm_End.strftime('%H:%M')
    }
    newEvent.update(recursos)
    
    index = BS_Date(evens, day)
    ev = []
    
    if index == -1:
        evens.append({
            "id": (day.year, day.month, day.day),
            "Lista_Eventos": [],
            "In_Time": True
        })
        ev = evens[len(evens)-1]["Lista_Eventos"]
    else:
        ev = evens[index]["Lista_Eventos"]
    
    if len(ev) == 0:
        ev.append(newEvent)
    else:
        index = len(ev)
        for i in range(len(ev)):
            hora = datetime.strptime(ev[i]["hora de inicio"], '%H:%M').time()
            if hora < tm_Init:
                index = i
                break
            elif hora == tm_Init and hora.minute < tm_Init.minute:
                index = i
                break
        ev.insert(index, newEvent)
    
    Sort_Dates(evens)
    data : dict = {}
    data["Eventos"] = evens
    data["Recursos"] = res
    Save_Data.SaveData(data)

def ViewDetails(event: dict, col) -> None:
    with col:
        st.markdown(f"**Descripcion**: {event["descripcion"]}")
        st.markdown("**Informacion de recursos ocupados**:")
        st.markdown(f"Sala: #{event["sala"]}")
        st.markdown(f"Tecnicos de Sonido: {event["tecnicos de sonido"]}")
        if "operadores de proyeccion" in event.keys():
            st.markdown(f"Operadores de Proyeccion: {event["operadores de proyeccion"]}")
        if "tecnicos de iluminacion" in event.keys():
            st.markdown(f"Tecnicos de Iluminacion: {event["tecnicos de iluminacion"]}")
        st.markdown(f"Personal de Limpieza: {event["personal de limpieza"]}")
        st.markdown(f"Personal de Seguridad: {event["personal de seguridad"]}")

def DeleteEvent(event: dict) -> None:
    event["activo"] = False
    data : dict = {}
    data["Eventos"] = evens
    data["Recursos"] = res
    Save_Data.SaveData(data)
#-----------------------------------------------------------------------------------------------------------
# Funciones auxiliares, para buscar y ordenar fechas
def BS_Date(l: list, d: date) -> int:
    if len(l) != 0:
        left = 0
        right = len(l)-1
        while left <= right:
            mid = (left + right)//2
            midDate = date(l[mid]["id"][0], l[mid]["id"][1], l[mid]["id"][2])
            if d == midDate: return mid
            elif d < midDate: right = mid - 1
            else: left = mid + 1
    return -1

def Sort_Dates(l: list) -> None:
    if len(l) <= 1: return
    mid = len(l)//2
    left = l[:mid]
    right = l[mid:]
    
    Sort_Dates(left)
    Sort_Dates(right)
    
    i, j, k = 0, 0, 0
    while i < len(left) and j < len(right):
        d1 = date(left[i]["id"][0], left[i]["id"][1], left[i]["id"][2])
        d2 = date(right[j]["id"][0], right[j]["id"][1], right[j]["id"][2])
        if d1 <= d2:
            l[k] = left[i]
            i+=1
        else:
            l[k] = right[j]
            j+=1
        k+=1
    
    while i < len(left):
        d1 = date(left[i]["id"][0], left[i]["id"][1], left[i]["id"][2])
        l[k] = left[i]
        i+=1
        k+=1
    while j < len(right):
        d2 = date(right[j]["id"][0], right[j]["id"][1], right[j]["id"][2])
        l[k] = right[j]
        j+=1
        k+=1