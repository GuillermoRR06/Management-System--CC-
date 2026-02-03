import streamlit as st
from datetime import *
from Functions import Save_Data
from Functions import AuxFuncs
#-----------------------------------------------------------------------------------------------------------
res = st.session_state["Recursos"]
evens = st.session_state["Eventos"]
# Funciones clave de la aplicacion: agregar, ver detalles y eliminar eventos
#-----------------------------------------------------------------------------------------------------------
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
    
    index = AuxFuncs.BS_Date(evens, day)
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
    
    AuxFuncs.Sort_Dates(evens)
    data : dict = {}
    data["Eventos"] = evens
    data["Recursos"] = res
    Save_Data.SaveData(data)
#-----------------------------------------------------------------------------------------------------------
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
#-----------------------------------------------------------------------------------------------------------
def DeleteEvent(event: dict) -> None:
    event["activo"] = False
    data : dict = {}
    data["Eventos"] = evens
    data["Recursos"] = res
    Save_Data.SaveData(data)
#-----------------------------------------------------------------------------------------------------------