import streamlit as st
from datetime import *
from Functions import RevResources, EventsFuncs, Save_Data
from Intellisense import Funcs
#-----------------------------------------------------------------------------------------------------------
if "Recursos" not in st.session_state or "Events" not in st.session_state:
    appData = Save_Data.GetData()
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
lugar, publico = 1, 1
tecSonido, opProyec, limpieza, seguridad, tecLight = 1, 1, 1, 1, 1
#-----------------------------------------------------------------------------------------------------------
if selection == tiposEventos[0]:
    # Seleccionar la fecha, la hora y la duracion del evento 
    col0, col1, col2 = st.columns([4, 4, 4])
    
    with col0:
        fecha = st.date_input("Seleccione la fecha 📅 del nuevo evento:", min_value=date.today()+timedelta(1), max_value=date.today()+timedelta(30))
    
    with col1:
        st.write("Ingrese la hora 🕑 del nuevo evento:")
        hr = st.number_input("Horas:", min_value=8, max_value=23)
        mint = st.slider("Minutos:", min_value=0, max_value=59)
        horaInicial = time(hour=hr, minute=mint)
        
    with col2:
        st.write("Ingrese la duracion del evento:")
        hr = horaInicial.hour + st.number_input("Horas:", min_value=0, max_value=4)
        if hr > 23: hr = hr % 24
        mint = horaInicial.minute + st.slider("Minutos:", min_value=1, max_value=59)
        if mint >= 60:
            mint = mint % 60
            hr += 1
            if hr > 23: hr = hr % 24
        horaFinal = time(hour=hr, minute=mint)
    
    recursos = RevResources.Disponibility(evens, fecha, horaInicial, horaFinal)
    st.markdown("---")
    #-------------------------------------------------------------------------------------------------------
    NotMC = RevResources.Check_MC(evens, fecha, horaInicial, horaFinal, True)
    if NotMC:
        # Seleccionar la cantidad de personas que asistiran al evento y la sala donde se efectuara 
        AllPlaces = RevResources.Check_Places(recursos["salas"], True)
        if AllPlaces:
            col3, col4 = st.columns([4, 4])
            with col3: publico = st.slider("Ingrese la cantidad de personas que asistiran al evento:", min_value=1, max_value=300)
            with col4: lugar = st.number_input("Ingrese la sala donde desea realizar el evento:", min_value=1, max_value=6)
            #-------------------------------------------------------------------------------------------------------
            # Asignar (por cantidad) al personal que trabajara en la sala escogida
            CorrectPlace = RevResources.Review_Place(lugar-1, recursos["salas"], True)
            AllPersonal = RevResources.Check_Personal(recursos, selection, True)
            if CorrectPlace and RevResources.Review_Capacity(salas[lugar-1], publico, True) and AllPersonal:
                st.markdown("## ")
                col5, col6, col7, col8 = st.columns([4, 4, 4, 4])
                with col5: tecSonido = st.number_input("Ingrese la cantidad de tecnicos de sonido 🔊 que necesite:", min_value=1, max_value=3, key=1)
                with col6: opProyec = st.number_input("Ingrese la cantidad de operadores de proyeccion 📽️ que necesite:", min_value=1, max_value=3, key=2)
                with col7: limpieza = st.number_input("Ingrese la cantidad de personal de limpieza 🧹 que necesite:", min_value=1, max_value=3, key=3)
                with col8: seguridad = st.number_input("Ingrese la cantidad de personal de seguridad 👮 que necesite:", min_value=1, max_value=3, key=4)
                necesidades = {
                    "sala": lugar,
                    "tecnicos de sonido": tecSonido,
                    "operadores de proyeccion": opProyec,
                    "personal de limpieza": limpieza,
                    "personal de seguridad": seguridad
                }
                
                #-------------------------------------------------------------------------------------------------------
                # Asignar un nombre o identificativo a la pelicula
                CorrectEmpls = RevResources.Review_Personal(recursos, necesidades, True)
                if CorrectEmpls and RevResources.Review_PersCapacity(limpieza, seguridad, publico, True) and RevResources.Review_PersPlace(tecSonido, opProyec, 0, lugar, True):
                    nombre = st.text_input("Ingresa el nombre de la pelicula:")
                    descripcion = st.text_area("Ingresa una descripcion del evento (opcional):", max_chars=144)
                    st.markdown("---")
                    if nombre != "" and st.button("▶️ Agregar Evento"):
                        EventsFuncs.AddEvent(evens, selection, fecha, horaInicial, horaFinal, nombre, descripcion, necesidades)
                        data : dict = {}
                        data["Eventos"] = evens
                        data["Recursos"] = res
                        Save_Data.SaveData(data)
    
    #En caso de que no sea posible agregar el evento en este horario, se recomienda otro horario                    
                elif not CorrectEmpls:
                    Funcs.FindNewHour_Film_Theather(evens, fecha, horaInicial, horaFinal, selection, lugar-1, necesidades)
            elif not (CorrectPlace and AllPersonal):
                necesidades = {
                    "sala": lugar,
                    "tecnicos de sonido": tecSonido,
                    "operadores de proyeccion": opProyec,
                    "personal de limpieza": limpieza,
                    "personal de seguridad": seguridad
                }
                Funcs.FindNewHour_Film_Theather(evens, fecha, horaInicial, horaFinal, selection, lugar-1, necesidades)
        else:
            necesidades = {
                "sala": lugar,
                "tecnicos de sonido": tecSonido,
                "operadores de proyeccion": opProyec,
                "personal de limpieza": limpieza,
                "personal de seguridad": seguridad
            }
            Funcs.FindNewHour_Film_Theather(evens, fecha, horaInicial, horaFinal, selection, lugar-1, necesidades)
    else:
        necesidades = {
            "sala": lugar,
            "tecnicos de sonido": tecSonido,
            "operadores de proyeccion": opProyec,
            "personal de limpieza": limpieza,
            "personal de seguridad": seguridad
        }
        Funcs.FindNewHour_Film_Theather(evens, fecha, horaInicial, horaFinal, selection, lugar-1, necesidades)
#-----------------------------------------------------------------------------------------------------------
if selection == tiposEventos[1]:
    # Seleccionar la fecha, la hora y la duracion del evento
    col0, col1, col2 = st.columns([4, 4, 4])
    with col0:
        fecha = st.date_input("Seleccione la fecha 📅 del nuevo evento:", min_value=date.today()+timedelta(1), max_value=date.today()+timedelta(30))
    
    with col1:
        st.write("Ingrese la hora 🕑 del nuevo evento:")
        hr = st.number_input("Horas:", min_value=8, max_value=23)
        mint = st.slider("Minutos:", min_value=0, max_value=59)
        horaInicial = time(hour=hr, minute=mint)
        
    with col2:
        st.write("Ingrese la duracion del evento:")
        hr = horaInicial.hour + st.number_input("Horas:", min_value=0, max_value=4)
        if hr > 23: hr = hr % 24
        mint = horaInicial.minute + st.slider("Minutos:", min_value=1, max_value=59)
        if mint >= 60:
            mint = mint % 60
            hr += 1
            if hr > 23: hr = hr % 24
        horaFinal = time(hour=hr, minute=mint)
        
    recursos = RevResources.Disponibility(evens, fecha, horaInicial, horaFinal)
    st.markdown("---")
    
    #-------------------------------------------------------------------------------------------------------
    NotMC = RevResources.Check_MC(evens, fecha, horaInicial, horaFinal, True)
    if NotMC:
        # Seleccionar la cantidad de personas que asistiran al evento y la sala donde se efectuara
        AllPlaces = RevResources.Check_Places(recursos["salas"], True)
        if AllPlaces:
            col3, col4 = st.columns([4, 4])
            with col3: publico = st.slider("Ingrese la cantidad de personas que asistiran al evento:", min_value=1, max_value=300)
            with col4: lugar = st.number_input("Ingrese la sala donde desea realizar el evento:", min_value=1, max_value=6)
        
            #-------------------------------------------------------------------------------------------------------
            # Asignar (por cantidad) al personal que trabajara en la sala escogida
            CorrectPlace = RevResources.Review_Place(lugar-1, recursos["salas"], True)
            AllPersonal = RevResources.Check_Personal(recursos, selection, True)
            if CorrectPlace and RevResources.Review_Scene(lugar-1, True) and RevResources.Review_Capacity(salas[lugar-1], publico, True) and AllPersonal:
                st.markdown("## ")
                col5, col6, col7, col8 = st.columns([4, 4, 4, 4])
                with col5: tecSonido = st.number_input("Ingrese la cantidad de tecnicos de sonido 🔊 que necesite:", min_value=1, max_value=3, key=1)
                with col6: tecLight = st.number_input("Ingrese la cantidad de tecnicos de iluminacion 💡 que necesite:", min_value=1, max_value=3, key=2)
                with col7: limpieza = st.number_input("Ingrese la cantidad de personal de limpieza 🧹 que necesite:", min_value=1, max_value=3, key=3)
                with col8: seguridad = st.number_input("Ingrese la cantidad de personal de seguridad 👮 que necesite:", min_value=1, max_value=3, key=4)
                necesidades = {
                    "sala": lugar,
                    "tecnicos de sonido": tecSonido,
                    "tecnicos de iluminacion": tecLight,
                    "personal de limpieza": limpieza,
                    "personal de seguridad": seguridad
                }
                #-------------------------------------------------------------------------------------------------------
                # Asignar un nombre o identificativo a la pelicula
                CorrectEmpls = RevResources.Review_Personal(recursos, necesidades, True)
                if CorrectEmpls and RevResources.Review_PersCapacity(limpieza, seguridad, publico, True) and RevResources.Review_PersPlace(tecSonido, 0, tecLight, lugar, True):
                    nombre = st.text_input("Ingresa el nombre de la obra teatral:")
                    descripcion = st.text_area("Ingresa una descripcion del evento (opcional):", max_chars=144)
                    st.markdown("---")
                    if nombre != "" and st.button("▶️ Agregar Evento"):
                        EventsFuncs.AddEvent(evens, selection, fecha, horaInicial, horaFinal, nombre, descripcion, necesidades)
                        data : dict = {}
                        data["Eventos"] = evens
                        data["Recursos"] = res
                        Save_Data.SaveData(data)
                        st.success("Evento agregado exitosamente")

    #En caso de que no sea posible agregar el evento en este horario, se recomienda otro horario                    
                elif not CorrectEmpls:
                    Funcs.FindNewHour_Film_Theather(evens, fecha, horaInicial, horaFinal, selection, lugar-1, necesidades)
            elif not (CorrectPlace and AllPersonal):
                necesidades = {
                    "sala": lugar,
                    "tecnicos de sonido": tecSonido,
                    "operadores de proyeccion": opProyec,
                    "personal de limpieza": limpieza,
                    "personal de seguridad": seguridad
                }
                Funcs.FindNewHour_Film_Theather(evens, fecha, horaInicial, horaFinal, selection, lugar-1, necesidades)
        else:
            necesidades = {
                "sala": lugar,
                "tecnicos de sonido": tecSonido,
                "operadores de proyeccion": opProyec,
                "personal de limpieza": limpieza,
                "personal de seguridad": seguridad
            }
            Funcs.FindNewHour_Film_Theather(evens, fecha, horaInicial, horaFinal, selection, lugar-1, necesidades)
    else:
        necesidades = {
            "sala": lugar,
            "tecnicos de sonido": tecSonido,
            "operadores de proyeccion": opProyec,
            "personal de limpieza": limpieza,
            "personal de seguridad": seguridad
        }
        Funcs.FindNewHour_Film_Theather(evens, fecha, horaInicial, horaFinal, selection, lugar-1, necesidades)
#-----------------------------------------------------------------------------------------------------------
if selection == tiposEventos[2]:
    # Seleccionar la fecha, la hora y la duracion del evento
    col0, col1, col2 = st.columns([4, 4, 4])
    
    with col0:
        fecha = st.date_input("Seleccione la fecha 📅 del nuevo evento:", min_value=date.today()+timedelta(1), max_value=date.today()+timedelta(30))
    
    with col1:
        st.write("Ingrese la hora 🕑 del nuevo evento:")
        hr = st.number_input("Horas:", min_value=8, max_value=23)
        mint = st.slider("Minutos:", min_value=0, max_value=59)
        horaInicial = time(hour=hr, minute=mint)
    
    with col2:
        st.write("Ingrese la duracion del evento:")
        hr = horaInicial.hour + st.number_input("Horas:", min_value=0, max_value=4)
        if hr > 23: hr = hr % 24
        mint = horaInicial.minute + st.slider("Minutos:", min_value=1, max_value=59)
        if mint >= 60:
            mint = mint % 60
            hr += 1
            if hr > 23: hr = hr % 24
        horaFinal = time(hour=hr, minute=mint)
        
    recursos = RevResources.Disponibility(evens, fecha, horaInicial, horaFinal)
    st.markdown("---")
    #-------------------------------------------------------------------------------------------------------
    NotOEvs = RevResources.Check_Evs(evens, fecha, horaInicial, horaFinal, True)
    if NotOEvs:
        # Seleccionar la cantidad de personas que asistiran al evento y la sala donde se efectuara
        col3, col4 = st.columns([4, 4])
        with col3: publico = st.slider("Ingrese la cantidad de personas que asistiran al evento:", min_value=1, max_value=300)
        with col4: lugar = st.number_input("Ingrese la sala donde desea realizar el evento:", min_value=1, max_value=6)
        #-------------------------------------------------------------------------------------------------------
        # Asignar (por cantidad) al personal que trabajara en la sala escogida
        if RevResources.Review_Scene(lugar-1, True) and RevResources.Review_Capacity(salas[lugar-1], publico, True):
            st.markdown("## ")
            col5, col6, col7, col8 = st.columns([4, 4, 4, 4])
            with col5: tecSonido = st.number_input("Ingrese la cantidad de tecnicos de sonido 🔊 que necesite:", min_value=1, max_value=3, key=1)
            with col6: tecLight = st.number_input("Ingrese la cantidad de tecnicos de iluminacion 💡 que necesite:", min_value=1, max_value=3, key=2)                
            with col7: limpieza = st.number_input("Ingrese la cantidad de personal de limpieza 🧹 que necesite:", min_value=1, max_value=3, key=3)
            with col8: seguridad = st.number_input("Ingrese la cantidad de personal de seguridad 👮 que necesite:", min_value=1, max_value=3, key=4)
            necesidades = {
                "sala": lugar,
                "tecnicos de sonido": tecSonido,
                "tecnicos de iluminacion": tecLight,
                "personal de limpieza": limpieza,
                "personal de seguridad": seguridad
            }
            #-------------------------------------------------------------------------------------------------------
            # Asignar un nombre o identificativo a la pelicula
            if RevResources.Review_PersCapacity(limpieza, seguridad, publico, True) and RevResources.Review_PersPlace(tecSonido, 0, tecLight, lugar, True):
                nombre = st.text_input("Ingresa el nombre del artista o los artistas:")
                descripcion = st.text_area("Ingresa una descripcion del evento (opcional):", max_chars=144)
                st.markdown("---")
                if nombre != "" and st.button("▶️ Agregar Evento"):
                    EventsFuncs.AddEvent(evens, selection, fecha, horaInicial, horaFinal, nombre, descripcion, necesidades)
                    data : dict = {}
                    data["Eventos"] = evens
                    data["Recursos"] = res
                    Save_Data.SaveData(data)
                    st.success("Evento agregado exitosamente")
                    
    #En caso de que no sea posible agregar el evento en este horario, se recomienda otro horario
    else:
        necesidades = {
            "sala": lugar,
            "tecnicos de sonido": tecSonido,
            "operadores de proyeccion": opProyec,
            "personal de limpieza": limpieza,
            "personal de seguridad": seguridad
        }
        Funcs.FindNewHour_Music(evens, fecha, horaInicial, horaFinal)