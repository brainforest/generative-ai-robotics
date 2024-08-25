from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "user", "content": "kısaca cevap verebilir misin : Galaksi nedir ?."}
  ]
)

print(completion.choices[0].message)
