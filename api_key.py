import streamlit as st

def get_api_key():
    st.subheader("Insira sua chave API")
    api_key = st.text_input("Chave API", type="password")
    if st.button("Salvar"):
        return api_key