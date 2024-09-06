import json
from openai import OpenAI

# Alice was born in London. She met Bob in Paris, where they discussed quantum mechanics. Alice works for Google, while Bob is a researcher at MIT. Alice loves hiking in the mountains, while Bob enjoys surfing. They both have a keen interest in AI and robotics.

# Define the knowledge base
knowledge_base = {
    "Alice": { "born_in": "London", "works_for": "Google", "loves": ["hiking"], "interests": ["AI and robotics"] },
    "Bob": { "works_at": "MIT", "enjoys": ["surfing"], "interests": ["AI and robotics"] },
    "London": { "type": "Location" },
    "Paris": { "type": "Location" },
    "Google": { "type": "Organization" },
    "MIT": { "type": "Organization" },
    "AI and robotics": { "type": "Interest" },
    "hiking": { "type": "Activity" },
    "surfing": { "type": "Activity" }
}

# Print the JSON formatted knowledge base
print(json.dumps(knowledge_base, indent=2))

def create_context(knowledge_base):
    context = []
    for entity, attributes in knowledge_base.items():
        context.append(f"Entity: {entity}")
        for key, value in attributes.items():
            if isinstance(value, list):
                context.append(f"  {key}: {', '.join(value)}")
            else:
                context.append(f"  {key}: {value}")
    return "\n".join(context)

# Generate context
context = create_context(knowledge_base)

# Print the context
print("\nContext for OpenAI API:\n")
print(context)

client = OpenAI()

def ask_openai_with_context(question, context):
    full_prompt = f"Given the following information:\n{context}\n\nAnswer the following question: {question}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": full_prompt}
        ]
    )
    return response.choices[0].message.content

# Example question
question = "What can you tell me about Alice's interests?"

print("You asked:",question)
# Get the answer from OpenAI
answer = ask_openai_with_context(question, context)
print("OpenAI Answer:", answer)

