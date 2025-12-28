import streamlit as st
import datetime as dt
#-----------------------------------------------------------------------------------------------------------
res = st.session_state["Recursos"]
evens = st.session_state["Eventos"]
salas = res["salas"]
#-----------------------------------------------------------------------------------------------------------
text = [
    "Este dia tiene varios horarios libres sin eventos. Aqui te recomiendo algunos:",
    "La sala () esta desocupada en estos horarios:",
    "Las salas () y () estan desocupadas en estos horarios:",
    "Las salas (), () y () estan desocupadas en estos horarios:",
    "Este dia no hay eventos programados. Sientete libre de escoger el horario.",
    "La manana esta completamente libre de eventos.",
    "La tarde esta completamente libre de eventos",
    "La noche esta completamente libre de eventos",
    "Hay poco personal disponible en este horario. Te recomiendo este otro horario mas liberado:",
    "Este dia esta demasiado agetreado, te recomiendo este otro dia para programar el evento:",
]
#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------