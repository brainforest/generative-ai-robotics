import json
from openai import OpenAI

client = OpenAI()

# Example usage with OpenAI API
def ask_openai_with_graph(question, document):
    full_prompt = f"Given the following information:\n{document}\n\nAnswer the following question: {question}"
    # OpenAI API call
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": full_prompt}
        ]
    )
    # Print the OpenAI response
    print(response.choices[0].message.content)

# Example document and question
document = """Alice was born in London. She met Bob in Paris, where they discussed quantum mechanics. 
Alice works for Google, while Bob is a researcher at MIT. Alice loves hiking in the mountains, 
while Bob enjoys surfing. They both have a keen interest in AI and robotics."""

question = "What can you tell me about Alice's career?"

if __name__ == "__main__":
    ask_openai_with_graph(question, document)
