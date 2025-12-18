import streamlit as st
#-----------------------------------------------------------------------------------------------------------
evens = st.session_state.get("Eventos")
#-----------------------------------------------------------------------------------------------------------
st.markdown("# Eventos Programados")
st.markdown("---")
#-----------------------------------------------------------------------------------------------------------
# Muestra todos los eventos programados en el periodo de tiempo actual
for e in evens:
    if e["In_Time"]:
        st.markdown(f"### {e["id"]}")
        for i in reversed(e["List_Events"]):
            if i["tipo"] == "Proyeccion Filmica":
                st.markdown(f"#### 🎥 {i["hora de inicio"]}-{i["hora de fin"]} | '{i["tipo"]}: {i["nombre"]}'")
            if i["tipo"] == "Obra de Teatro":
                st.markdown(f"#### 🎭​ {i["hora de inicio"]}-{i["hora de fin"]} | '{i["tipo"]}: {i["nombre"]}'")
            if i["tipo"] == "Concierto Musical":
                st.markdown(f"#### ​🎸 {i["hora de inicio"]}-{i["hora de fin"]} | '{i["tipo"]}: {i["nombre"]}'")
        st.markdown("---")