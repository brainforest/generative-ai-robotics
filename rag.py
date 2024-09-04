from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI()

# Mock search function simulating document retrieval
def search_documents(query):
    # Simulated documents
    documents = [
        "Python is a popular programming language known for its simplicity.",
        "The OpenAI API allows developers to integrate advanced language models into their applications.",
        "Machine learning models can be fine-tuned for specific tasks."
    ]
    # In a real-world scenario, you'd use a search engine or database query here
    return [doc for doc in documents if query.lower() in doc.lower()]

# RAG Process
def rag_example(user_query):
    # Step 1: Retrieve relevant documents
    retrieved_docs = search_documents(user_query)

    # Step 2: Create a context-rich prompt
    context = "\n".join(retrieved_docs)
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
user_query = "Tell me about the OpenAI API."
response = rag_example(user_query)
print("RAG Response:", response)
