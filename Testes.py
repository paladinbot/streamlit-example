import streamlit as st

# Suponha que 'tempo' seja o tempo usado para a análise
tempo = 10

# Cria o primeiro botão
if st.button('Mostrar Tempo'):
    # Escreve a mensagem
    st.write('Tempo usado para a análise: ', tempo, 'segundos')

# Cria o segundo botão
if st.button('Esconder Tempo'):
    # Limpa a tela
    st.empty()
    