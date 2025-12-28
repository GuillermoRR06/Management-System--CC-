import streamlit as st
from Functions import Save_Data
#-----------------------------------------------------------------------------------------------------------
if "Recursos" not in st.session_state or "Events" not in st.session_state:
    appData = Save_Data.GetData(Save_Data.Get_Timestamp())
#-----------------------------------------------------------------------------------------------------------
res = st.session_state.get("Recursos")
#-----------------------------------------------------------------------------------------------------------
st.markdown("# Informacion de Recursos del Teatro")
st.markdown("---")
#-----------------------------------------------------------------------------------------------------------
st.markdown("## Salas")
for k in res["salas"]:
    st.markdown(f"### Sala #{k["id"]}")
    col1, col2 = st.columns([2, 2])
    with col1: st.markdown(f"**Capacidad** -> *{k["capacidad"]}* butacas")
    with col2:
        st.markdown("**Recursos Asociados:**")
        for i in k["recursos_asociados"]: st.markdown(f"*{i.capitalize()}*")
st.markdown("---")
#-----------------------------------------------------------------------------------------------------------
st.markdown("## Personal")
for k in res["humanos"].keys():
    st.markdown(f"### {k.capitalize()}")
    st.markdown(f"**Cantidad** -> *{res["humanos"][k]}*")
