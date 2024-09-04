from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI()

# Simple knowledge graph using a dictionary
knowledge_graph = {
    "Python": {
        "description": "Python is a popular programming language known for its simplicity.",
        "creator": "Guido van Rossum",
        "released": "1991"
    },
    "OpenAI API": {
        "description": "The OpenAI API allows developers to integrate advanced language models into their applications.",
        "usage": "Used for generating natural language responses, fine-tuning models, and more."
    }
}

# Knowledge Graph Process
def knowledge_graph_example(user_query):
    # Step 1: Extract relevant information from the knowledge graph
    context = ""
    for key, info in knowledge_graph.items():
        if key.lower() in user_query.lower():
            context += f"{key}: {info['description']}\n"

    # Step 2: Create a context-rich prompt
    prompt = f"Given the following information:\n{context}\n\nAnswer the following question: {user_query}"

    # Step 3: Send the prompt to OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
           {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message

# Example Usage
user_query = "Tell me about Python."
response = knowledge_graph_example(user_query)
print("Knowledge Graph Response:", response)

