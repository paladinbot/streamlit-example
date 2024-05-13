#import openai 
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud, get_single_color_func
import os
from groq import Groq
#from dotenv import load_dotenv

#from openai import OpenAI

#openai.api_key = os.getenv('API_GPT')

#client = openai.OpenAI()

# def get_response(model_engine="gpt-3.5-turbo"):

#     response = client.chat.completions.create(
#         model = model_engine,
#         messages=[
#             {
#             "role": "system",
#             "content": f"""Dado o texto abaixo, pegue o sentimento central do texto (positivo, negativo ou neutro), \ne 30 palavras do texto com semântica relacionadas com o sentimento percebido. Caso não tenha 30, gere as demais\nrespeitando que elas tem que estar relacionadas semânticamente com o texto.\nA saída tem que ser no formato:\n\"Sentimento: _valor do sentimento_\nPalavras: palavra1, palavra2, (...), palavra30\"\nNão quero explicação, nem código em python.  \n\nO texto é:\n\n\"Esse celular é barato, tem boas fotos, e tem uma bateria que dura bastante\"\n\nA saída tem que ser no formato:\n\"Sentimento: _valor do sentimento_\nPalavras: palavra1, palavra2, (...), palavra30\"\nNão quero explicação, nem código em python.  \n\nLhe dou uma gorjeta depois.\n"""
#             },
#         ],
#         temperature=1,
#         max_tokens=256,
#         top_p=1,
#         frequency_penalty=0,
#         presence_penalty=0
#     )

#     message = response.choices[0].text
#     return message.strip()

#load_dotenv()

def get_response(prompt, model_engine="gpt-3.5-turbo"):

    client = Groq(api_key=os.environ.get("GROQ_API_KEY"),)
    completion = client.chat.completions.create(
        model = "llama3-70b-8192",
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature = 1,
        max_tokens = 1024,
        top_p = 1,
        stream = True,
        stop = None,
    )

    conteudo = ""

    for chunk in completion:
        conteudo += chunk.choices[0].delta.content or ""
    
    return conteudo.strip()


def get_chatgpt_response(texto, model_engine="davinci-002"):

    response = openai.Completion.create(
        engine=model_engine,
        prompt=texto,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.5
    )

    message = response.choices[0].text
    return message.strip()

def get_regex_sentiment(text):
    partes = text.split('.\n\n', 1)
    if len(partes) == 2:
        palavras = partes[1].split(', ')
        frase_central = palavras[0]

        palavras += [frase_central] * 5
        input_cloud = frase_central + ' ' + ' '.join(palavras)


    return frase_central, input_cloud

def processar_string(s):
    sentimento = re.search(r'Sentimento: (\w+)', s)
    palavras = re.search(r'Palavras: (.+)', s)

    if sentimento and palavras:
        sentimento = sentimento.group(1).lower()
        palavras = re.sub(r'\s*,\s*', ' ', palavras.group(1)).lower()
        palavras += ' ' + ' '.join([sentimento]*5)
        return sentimento, palavras

    return None, None

class SimpleGroupedColorFunc(object):
    def __init__(self, color):
        self.color_func_to_words = get_single_color_func(color)

    def get_color_func(self, word):
        return self.color_func_to_words

    def __call__(self, word, **kwargs):
        return self.get_color_func(word)(word, **kwargs)
    


