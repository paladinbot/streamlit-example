__version__ = "1.0.0.0"
app_name = "Multsent"

import streamlit as st
from wordcloud import WordCloud
from util import get_chatgpt_response, get_regex_sentiment, SimpleGroupedColorFunc, processar_string, get_response
from api_key import get_api_key
import matplotlib.pyplot as plt
import time
	
tempo = 0
sentimento = ''
input_cloud = ''

#st.title("MultSent : Análise de Sentimentos")
# st.write(" ")
# st.write(" ")
# st.write(" ")
# st.write(" ")
# st.write(" ")
# st.write(" ")
# st.write(" ")
# st.write(" ")

st.subheader("Preencha os dados abaixo para realizar a sua classificação")

#page = st.sidebar.selectbox("Escolha uma página", ["Página Principal", "Inserir Chave API"])

def get_world_cloud(text, color_func):
    wordcloud = WordCloud(width=800, height=400, background_color='white', color_func=color_func).generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


def ui_spacer(n=2, line=False, next_n=0):
	for _ in range(n):
		st.write('')
	if line:
		st.tabs([' '])
	for _ in range(next_n):
		st.write('')

def ui_info():
	# Carregar a imagem
	image = 'imgs/logo.png'

	# Inserir a imagem no app Streamlit
	st.image(image, use_column_width=True)
	st.markdown(f"""
	# Multsent
	versão {__version__}
	
	Ferramenta de Classificação de Sentimento utilizando LLMs. 
	""")
	ui_spacer(1)
	st.write("Feito por [Yuri Herbert](https://www.linkedin.com/in/yuri-herbert-5a3952109/).", unsafe_allow_html=True)
	ui_spacer(1)
	st.markdown("""
		Obrigado pelo seu interesse na minha aplicação.
		Esteja atento que essa é apenas uma prova de conceito 
		para a disciplina de Projeto Final Integrador 2 
		da [Universidade de Fortaleza](https://www.unifor.br/)
		e pode conter alguns bugs e features incompletas.
		Se você gostar desse app você pode [me seguir](https://twitter.com/Yur1Herbert)
		no Twitter para novidades e atualizações.
		""")
	ui_spacer(1)
	st.markdown('O código fonte pode ser encontrado [aqui](https://github.com/mobarski/ask-my-pdf).')

model = st.selectbox(
    "Selecione o modelo",
    ("llama3-8b-8192", "llama3-70b-8192", "gemma-7b-it", "mixtral-8x7b-32768")
)

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

query = st.text_area("Insira sua sentença: ", key="input")

sub = st.button('Processar')


if sub:
    texto_prompt=f"""Dado o texto abaixo, pegue o sentimento central do texto (positivo, negativo ou neutro), 
e 30 palavras do texto com semântica relacionadas com o sentimento percebido. Caso não tenha 30, gere as demais
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
        #response = get_chatgpt_response(texto_prompt)
        response = get_response(texto_prompt, model)
        end = time.time()
        tempo = round(end-start, 2)
        st.session_state.past.append(query)
        st.session_state.generated.append(response)
        st.session_state.generated.append(tempo)
		
with st.sidebar:
	ui_info()

if st.session_state['generated']:
	st.write('Tempo usado para a análise: ', st.session_state.generated[1], 'segundos')
	submit = st.button('Ver sentimento e nuvem de palavras')
	if submit:
		st.empty()
		sentimento, input_cloud = processar_string(st.session_state.generated[0])
		#print(sentimento)
		#sentimento = sentimento.lower()
		st.write(processar_string(st.session_state.generated[0]))
		#st.write("o que vai gerar as palavras do wordcloud: " + input_cloud)
		#st.write(sentimento)
		#st.write(model)

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
		

