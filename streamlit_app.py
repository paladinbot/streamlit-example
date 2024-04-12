import streamlit as st
from wordcloud import WordCloud
from util import get_chatgpt_response, get_regex_sentiment, SimpleGroupedColorFunc, processar_string
import matplotlib.pyplot as plt
import time

tempo = 0
sentimento = ''
input_cloud = ''
st.title("MultSent : Análise de Sentimentos")
st.subheader("Preencha os dados abaixo para realizar a sua análise")

def get_world_cloud(text, color_func):
    wordcloud = WordCloud(width=800, height=400, background_color='white', color_func=color_func).generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

model = st.selectbox(
    "Selecione o modelo",
    ("gpt-3.5", "llama-2", "bloom")
)

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

query = st.text_area("Insira sua sentença: ", key="input")

sub = st.button('Processar a Sentença')


if sub:
    texto_prompt=f"""Dado o texto abaixo, pegue o sentimento central do texto (positivo, negativo ou neutro), 
e até 30 palavras do texto com semântica relacionadas com o sentimento percebido. Caso não tenha 30, gere as demais
respeitando que elas tem que estar relacionadas semânticamente com o texto.
A saída tem que ser no formato:
"Sentimento: _valor do sentimento_\nPalavras: palavra1, palavra2, (...), palavra30"
Não quero explicação, nem código em python.  

O texto é:

"{query}"

A saída tem que ser no formato:
"Sentimento: _valor do sentimento_\nPalavras: palavra1, palavra2, (...), palavra30"
Não quero explicação, nem código em python.  

Lhe dou uma gorjeta depois.

"""
   
    with st.spinner("generating..."):
        start = time.time()
        response = get_chatgpt_response(texto_prompt)
        end = time.time()
        tempo = round(end-start, 2)
        st.session_state.past.append(query)
        st.session_state.generated.append(response)
        st.session_state.generated.append(tempo)
		

        
if st.session_state['generated']:
	st.write('Tempo usado para a análise: ', st.session_state.generated[1], 'segundos')
	submit = st.button('Ver sentimentos e nuvem de palavras')
	if submit:
		st.empty()
		sentimento, input_cloud = processar_string(st.session_state.generated[0])
		sentimento = sentimento.lower()
		st.write(processar_string(st.session_state.generated[0]))
		#st.write("o que vai gerar as palavras do wordcloud: " + input_cloud)
		st.write(sentimento)

		if(sentimento == "positivo"):            
			wordcloud = WordCloud(width=800, height=400, background_color='white', color_func=SimpleGroupedColorFunc('green')).generate(input_cloud)
		elif(sentimento == "neutro"):   
			wordcloud = WordCloud(width=800, height=400, background_color='white', color_func=SimpleGroupedColorFunc('yellow')).generate(input_cloud) 
		else:
			wordcloud = WordCloud(width=800, height=400, background_color='white', color_func=SimpleGroupedColorFunc('red')).generate(input_cloud)     
		fig, ax = plt.subplots(figsize = (12, 8))
		ax.imshow(wordcloud)
		plt.axis("off")
		st.pyplot(fig)

		st.session_state['generated'] = []
		st.session_state['past'] = []
		

