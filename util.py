import openai 
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud, get_single_color_func
import os

#openai.api_key = os.getenv('API_GPT')
openai.api_key = 65

def get_chatgpt_response(texto, model_engine="text-davinci-003"):

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
    


