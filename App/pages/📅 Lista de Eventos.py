import streamlit as st
import datetime as dt
from Functions import EventsFuncs, RevResources, AuxFuncs, Save_Data
#-----------------------------------------------------------------------------------------------------------
if "Recursos" not in st.session_state or "Events" not in st.session_state:
    appData = Save_Data.GetData()
#-----------------------------------------------------------------------------------------------------------
evens = st.session_state.get("Eventos")
day = st.session_state.fecha
#-----------------------------------------------------------------------------------------------------------
st.markdown("# Eventos Programados")
st.markdown("---")
#-----------------------------------------------------------------------------------------------------------
daysList = ["Todos los dias"]
j = 0
for i in range(31):
    d = dt.date.today() + dt.timedelta(i)
    if st.session_state.mostrar and d.strftime('%B, %d, %Y') == day.strftime('%B, %d, %Y'): j = i+1
    daysList.append(d.strftime('%B, %d, %Y'))
selection = st.selectbox("Seleccione el dia del cual desea ver los eventos programados:", daysList, index=j)
st.markdown("---")
#-----------------------------------------------------------------------------------------------------------
# Opcion: *Un dia seleccionado* -> Muestra todos los eventos programados en el dia especifico seleccionado
k = 0
if selection != "Todos los dias" or st.session_state.mostrar:
    index = 0
    if st.session_state.mostrar:
        index = AuxFuncs.BS_Date(evens, st.session_state.fecha)
        st.session_state.mostrar = False
        st.session_state.fecha = dt.date.today() - dt.timedelta(1)
    else: index = AuxFuncs.BS_Date(evens, dt.datetime.strptime(selection, '%B, %d, %Y').date())
    if index == -1:
        st.markdown("### No hay eventos programados para este dia")
    elif not RevResources.Review_Events(evens[index]["Lista_Eventos"]):
        st.markdown("### No hay eventos programados para este dia")
    else:
        d = dt.date(evens[index]["id"][0], evens[index]["id"][1], evens[index]["id"][2])
        st.markdown(f"### {d.strftime('%B, %d, %Y')}")
        col1, col2, col3 = st.columns([3, 1, 1])
        for i in reversed(evens[index]["Lista_Eventos"]):
            if i["activo"]:
                if i["tipo"] == "Proyeccion Filmica":
                    with col1: st.markdown(f"#### 🎬 {i["hora de inicio"]}-{i["hora de fin"]} | '{i["tipo"]}: {i["nombre"]}'")
                    with col2:
                        if st.button("​🔍 Ver Detalles​", key=k): EventsFuncs.ViewDetails(i, col1)
                        k += 1
                    with col3:
                        if st.button("🗑️ Eliminar", key=k): EventsFuncs.DeleteEvent(i)
                        k += 1
                if i["tipo"] == "Obra de Teatro":
                    with col1: st.markdown(f"#### 🎭​ {i["hora de inicio"]}-{i["hora de fin"]} | '{i["tipo"]}: {i["nombre"]}'")
                    with col2:
                        if st.button("​🔍 Ver Detalles​", key=k): EventsFuncs.ViewDetails(i, col1)
                        k += 1
                    with col3:
                        if st.button("🗑️ Eliminar", key=k): EventsFuncs.DeleteEvent(i)
                        k += 1
                if i["tipo"] == "Concierto Musical":
                    with col1: st.markdown(f"#### ​🎶 {i["hora de inicio"]}-{i["hora de fin"]} | '{i["tipo"]}: {i["nombre"]}'")
                    with col2:
                        if st.button("​🔍 Ver Detalles​", key=k): EventsFuncs.ViewDetails(i, col1)
                        k += 1
                    with col3:
                        if st.button("🗑️ Eliminar", key=k): EventsFuncs.DeleteEvent(i)
                        k += 1
        st.markdown("---")
#-----------------------------------------------------------------------------------------------------------
# Opcion: "Todos los eventos" -> Muestra todos los eventos programados en el periodo de tiempo actual
else:
    for e in evens:
        if e["In_Time"] and RevResources.Review_Events(e["Lista_Eventos"]):
            d = dt.date(e["id"][0], e["id"][1], e["id"][2]).strftime('%B, %d, %Y')
            st.markdown(f"### {d}")
            col1, col2, col3 = st.columns([3, 1, 1])
            for i in reversed(e["Lista_Eventos"]):
                if i["activo"]:
                    if i["tipo"] == "Proyeccion Filmica":
                        with col1: st.markdown(f"#### 🎬 {i["hora de inicio"]}-{i["hora de fin"]} | '{i["tipo"]}: {i["nombre"]}'")
                        with col2:
                            if st.button("​🔍 Ver Detalles​", key=k): EventsFuncs.ViewDetails(i, col1)
                            k += 1
                        with col3:
                            if st.button("🗑️ Eliminar", key=k): EventsFuncs.DeleteEvent(i)
                            k += 1
                    if i["tipo"] == "Obra de Teatro":
                        with col1: st.markdown(f"#### 🎭​ {i["hora de inicio"]}-{i["hora de fin"]} | '{i["tipo"]}: {i["nombre"]}'")
                        with col2:
                            if st.button("​🔍 Ver Detalles​", key=k): EventsFuncs.ViewDetails(i, col1)
                            k += 1
                        with col3:
                            if st.button("🗑️ Eliminar", key=k): EventsFuncs.DeleteEvent(i)
                            k += 1
                    if i["tipo"] == "Concierto Musical":
                        with col1: st.markdown(f"#### ​🎶 {i["hora de inicio"]}-{i["hora de fin"]} | '{i["tipo"]}: {i["nombre"]}'")
                        with col2:
                            if st.button("​🔍 Ver Detalles​", key=k): EventsFuncs.ViewDetails(i, col1)
                            k += 1
                        with col3:
                            if st.button("🗑️ Eliminar", key=k): EventsFuncs.DeleteEvent(i)
                            k += 1
            st.markdown("---") 