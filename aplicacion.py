import streamlit as st

from workflow import app

st.set_page_config(
    page_title="Victory AI",
    page_icon=""
)

st.title(" Victory AI")
st.write("Asistente virtual de soporte para la tienda Victory.")

pregunta = st.text_input("Escribí tu consulta:")

if st.button("Enviar"):

    if pregunta.strip():

        resultado = app.invoke(
            {
                "pregunta": pregunta
            }
        )

        st.markdown("### Respuesta")
        st.write(resultado["respuesta"])

    else:
        st.warning("Ingresá una consulta.")