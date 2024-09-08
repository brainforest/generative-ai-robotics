import json
from openai import OpenAI

client = OpenAI()

def ask_openai_with_context(question):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.1,
        messages=[
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

# Example question
question = "In simple terms, explain how solar panels generate electricity. Please focus on the physics behind it, and use bullet points for clarity."

print("You asked:",question)
# Get the answer from OpenAI
answer = ask_openai_with_context(question )
print("OpenAI Answer:", answer)

