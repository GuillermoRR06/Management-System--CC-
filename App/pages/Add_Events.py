import streamlit as st
from datetime import *
from Functions import RevisarRecursos
from Functions import Save_Data
#-----------------------------------------------------------------------------------------------------------
res = st.session_state["Recursos"]
evens = st.session_state["Eventos"]

salas = res["salas"]
#-----------------------------------------------------------------------------------------------------------
st.markdown("# Agregar nuevos eventos")
st.markdown("---")
#-----------------------------------------------------------------------------------------------------------
# Seleccionar el evento que se desea programar
tiposEventos = ["Proyeccion Filmica", "Obra de Teatro", "Concierto Musical"]
selection = st.selectbox("Seleccione el evento que desea agregar:", tiposEventos)
st.markdown("---")
necesidades = {}
#-----------------------------------------------------------------------------------------------------------
if selection == tiposEventos[0]:
    # Seleccionar la fecha, la hora y la duracion del evento
    col0, col1, col2 = st.columns([4, 4, 4])
    with col0: fecha = st.date_input("Seleccione la fecha del nuevo evento:", min_value=date.today(), max_value=date.today()+timedelta(30))
    with col1: horaInicial = st.time_input("Seleccione la hora del nuevo evento:")
    with col2:
        st.write("Ingrese la duracion del evento:")
        horaFinal = time(
        hour=horaInicial.hour + st.number_input("Horas:", min_value=0, max_value=4),
        minute=horaInicial.minute + st.number_input("Minutos:", min_value=1, max_value=59))
    recursos = RevisarRecursos.Disponibility(evens, fecha, horaInicial)
    st.markdown("---")
    
    # Seleccionar la cantidad de personas que asistiran al evento y la sala donde se efectuara
    col3, col4 = st.columns([4, 4])
    lugar, publico = 0, 0
    with col3: publico = st.slider("Ingrese la cantidad de personas que asistiran al evento:", min_value=1, max_value=300)
    with col4: lugar = st.number_input("Ingrese la sala donde desea realizar el evento:", min_value=1, max_value=6)
    
    # Asignar (por cantidad) al personal que trabajara en la sala escogida
    if RevisarRecursos.Review_Place(lugar-1, recursos["salas"]) and RevisarRecursos.Review_Capacity(salas[lugar-1], publico):
        st.markdown("## ")
        col5, col6, col7, col8 = st.columns([4, 4, 4, 4])
        tecSonido, opProyec, limpieza, seguridad = 0, 0, 0, 0
        with col5: tecSonido = st.number_input("Ingrese la cantidad de tecnicos de sonido que necesite:", min_value=1, max_value=3, key=1)
        with col6: opProyec = st.number_input("Ingrese la cantidad de tecnicos de sonido que necesite:", min_value=1, max_value=3, key=2)
        with col7: limpieza = st.number_input("Ingrese la cantidad de personal de limpieza que necesite:", min_value=1, max_value=3, key=3)
        with col8: seguridad = st.number_input("Ingrese la cantidad de personal de seguridad que necesite:", min_value=1, max_value=3, key=4)
        necesidades = {
            "sala": lugar,
            "tecnicos de sonido": tecSonido,
            "operadores de proyeccion": opProyec,
            "personal de limpieza": limpieza,
            "personal de seguridad": seguridad
        }
        
        # Asignar un nombre o identificativo a la pelicula
        if RevisarRecursos.Review_Filme(recursos, necesidades):
            nombre = st.text_input("Ingresa el nombre de la pelicula:")
            st.markdown("---")
            if nombre != "" and st.button("Agregar Evento"):
                RevisarRecursos.AddEvent(evens, selection, fecha, horaInicial, horaFinal, nombre, necesidades)
                data : dict = {}
                data["Eventos"] = evens
                data["Recursos"] = res
                Save_Data.SaveData(data)
        
#-----------------------------------------------------------------------------------------------------------
if selection == tiposEventos[1]:
    col3, col4 = st.columns([4, 4])
    with col3: publico = st.slider("Ingrese la cantidad de personas que asistiran al evento:", min_value=1, max_value=300)
    with col4: lugar = st.number_input("Ingrese la sala donde desea realizar el evento:", min_value=1, max_value=6)
#-----------------------------------------------------------------------------------------------------------
if selection == tiposEventos[2]:
    col3, col4 = st.columns([4, 4])
    with col3: publico = st.slider("Ingrese la cantidad de personas que asistiran al evento:", min_value=1, max_value=300)
    with col4: lugar = st.number_input("Ingrese la sala donde desea realizar el evento:", min_value=1, max_value=6)
