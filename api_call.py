from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()

completion = client.chat.completions.create(
    model = "llama3-70b-8192",
    messages = [
        {
            "role": "user",
            "content": "Me explique o conceito da área de um círculo, e por que área de uma circunferencia não faz sentido"
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

print(conteudo)

