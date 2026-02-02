import streamlit as st
from Functions import Save_Data
#-----------------------------------------------------------------------------------------------------------
if "Recursos" not in st.session_state or "Events" not in st.session_state:
    appData = Save_Data.GetData()
#-----------------------------------------------------------------------------------------------------------
res = st.session_state.get("Recursos")
#-----------------------------------------------------------------------------------------------------------
st.markdown("# Informacion de Recursos del Teatro")
st.markdown("---")
#-----------------------------------------------------------------------------------------------------------
st.markdown("## Salas")
row1 = st.columns([2, 2, 2, 2])
st.markdown("# ")
row2 = st.columns([2, 2, 2, 2])
st.markdown("# ")
row3 = st.columns([2, 2, 2, 2])
salas = res["salas"]

with row1[0]: st.markdown(f"### Sala #{salas[0]["id"]}")
with row1[1]:
    st.markdown(f"**Capacidad** -> *{salas[0]["capacidad"]}* butacas")
    st.markdown("**Recursos Asociados:**")
    for i in salas[0]["recursos_asociados"]: st.markdown(f"*{i.capitalize()}*")
    st.markdown("**Personal Necesario:**")
    for i in salas[0]["necesita"]: st.markdown(f"*{i.capitalize()}*")

with row1[2]: st.markdown(f"### Sala #{salas[1]["id"]}")
with row1[3]:
    st.markdown(f"**Capacidad** -> *{salas[1]["capacidad"]}* butacas")
    st.markdown("**Recursos Asociados:**")
    for i in salas[1]["recursos_asociados"]: st.markdown(f"*{i.capitalize()}*")
    st.markdown("**Personal Necesario:**")
    for i in salas[1]["necesita"]: st.markdown(f"*{i.capitalize()}*")

with row2[0]: st.markdown(f"### Sala #{salas[2]["id"]}")
with row2[1]:
    st.markdown(f"**Capacidad** -> *{salas[2]["capacidad"]}* butacas")
    st.markdown("**Recursos Asociados:**")
    for i in salas[2]["recursos_asociados"]: st.markdown(f"*{i.capitalize()}*")
    st.markdown("**Personal Necesario:**")
    for i in salas[2]["necesita"]: st.markdown(f"*{i.capitalize()}*")

with row2[2]: st.markdown(f"### Sala #{salas[3]["id"]}")
with row2[3]:
    st.markdown(f"**Capacidad** -> *{salas[3]["capacidad"]}* butacas")
    st.markdown("**Recursos Asociados:**")
    for i in salas[3]["recursos_asociados"]: st.markdown(f"*{i.capitalize()}*")
    st.markdown("**Personal Necesario:**")
    for i in salas[3]["necesita"]: st.markdown(f"*{i.capitalize()}*")

with row3[0]: st.markdown(f"### Sala #{salas[4]["id"]}")
with row3[1]:
    st.markdown(f"**Capacidad** -> *{salas[4]["capacidad"]}* butacas")
    st.markdown("**Recursos Asociados:**")
    for i in salas[4]["recursos_asociados"]: st.markdown(f"*{i.capitalize()}*")
    st.markdown("**Personal Necesario:**")
    for i in salas[4]["necesita"]: st.markdown(f"*{i.capitalize()}*")

with row3[2]: st.markdown(f"### Sala #{salas[5]["id"]}")
with row3[3]:
    st.markdown(f"**Capacidad** -> *{salas[5]["capacidad"]}* butacas")
    st.markdown("**Recursos Asociados:**")
    for i in salas[5]["recursos_asociados"]: st.markdown(f"*{i.capitalize()}*")
    st.markdown("**Personal Necesario:**")
    for i in salas[5]["necesita"]: st.markdown(f"*{i.capitalize()}*")

st.markdown("---")
#-----------------------------------------------------------------------------------------------------------
st.markdown("## Personal")
row4 = st.columns([2, 2, 2, 2, 2])
empls = list(res["humanos"].keys())

with row4[0]:
    st.markdown(f"### {empls[0].capitalize()}")
    st.markdown(f"**Cantidad** -> *{res["humanos"][empls[0]]}*")
with row4[1]:
    st.markdown(f"### {empls[1].capitalize()}")
    st.markdown(f"**Cantidad** -> *{res["humanos"][empls[1]]}*")
with row4[2]:
    st.markdown(f"### {empls[2].capitalize()}")
    st.markdown(f"**Cantidad** -> *{res["humanos"][empls[2]]}*")
with row4[3]:
    st.markdown(f"### {empls[3].capitalize()}")
    st.markdown(f"**Cantidad** -> *{res["humanos"][empls[3]]}*")
with row4[4]:
    st.markdown(f"### {empls[4].capitalize()}")
    st.markdown(f"**Cantidad** -> *{res["humanos"][empls[4]]}*")

