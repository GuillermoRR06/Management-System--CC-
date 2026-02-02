import streamlit as st
import json
import datetime as dt
from Functions import Save_Data
#-----------------------------------------------------------------------------------------------------------
if "Recursos" not in st.session_state or "Events" not in st.session_state:
    appData = Save_Data.GetData()
#-----------------------------------------------------------------------------------------------------------
st.set_page_config(layout="wide")
#-----------------------------------------------------------------------------------------------------------
today = dt.date.today()
for e in appData["Eventos"]:
    d = dt.date(e["id"][0], e["id"][1], e["id"][2])
    if d < today:
        e["In_Time"] = False
    else: break
    
if len(appData["Eventos"]) >= 40:
    for e in appData["Eventos"]:
        if not e["In_Time"]:
            appData["Eventos"].remove(e)
Save_Data.SaveData(appData)
#-----------------------------------------------------------------------------------------------------------
st.session_state["Recursos"] = appData["Recursos"]
st.session_state["Eventos"] = appData["Eventos"]
#-----------------------------------------------------------------------------------------------------------
st.markdown("# Gestor de Eventos del Centro Cultural *La Cuarta Pared*")
st.markdown("---")

row1 = st.columns([2, 2, 2])
with row1[1]: st.image("App\Gallery\Logo.png", caption="✨ La Cuarta Pared no se mira… se vive.", width=500)

st.markdown("La Cuarta Pared no es solo un cine-teatro: es un punto de impacto cultural, un espacio moderno donde las historias saltan de la pantalla, el escenario vibra con cada aplauso y la música en vivo te sacude el alma.")
st.markdown("Todo en un ambiente moderno, eléctrico y diseñado para todo público, donde cada función es un evento y cada noche se convierte en un recuerdo. Entra, apaga el mundo por un rato y deja que el espectáculo haga el resto.")
st.markdown("🚪 Rompe la barrera entre tú y el escenario.")
st.markdown("🚀 Sal distinto de como entraste.")
st.markdown("✨ La Cuarta Pared: no mires el arte… deja que te mire a ti.")

st.markdown("---")
st.markdown("Aquí no vienes a “ver un show”.")
st.markdown("Vienes a **vivir una experiencia**.")

row2 = st.columns([2, 2, 2])
with row2[0]: st.image("App\Gallery\Movie_Screening.jpg", caption="🎬 Películas que te atrapan.", width=350)
with row2[1]: st.image("App\Gallery\Theather_Play.jpg", caption="🎭 Obras que te confrontan.", width=350)
with row2[2]: st.image("App\Gallery\Musical_Concert.jpg", caption="🎶 Conciertos que te atraviesan el pecho.", width=350)

