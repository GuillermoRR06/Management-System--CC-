import streamlit as st
#-----------------------------------------------------------------------------------------------------------
evens = st.session_state.get("Eventos")
#-----------------------------------------------------------------------------------------------------------
st.markdown("# Eventos Programados")
st.markdown("---")
#-----------------------------------------------------------------------------------------------------------
for e in evens:
    st.markdown(f"### {list(e.keys())[0]}")
    for i in e[list(e.keys())[0]]:
        st.markdown(f"#### {chr(16)} {i["hora de inicio"]}-{i["hora de fin"]} | '{i["tipo"]}: {i["nombre"]}'")
    st.markdown("---")