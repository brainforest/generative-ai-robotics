import faiss
import numpy as np
import openai

# Example documents to store in memory
documents = [
    "The sun is the star at the center of the solar system.",
    "Solar energy is renewable and can reduce carbon emissions.",
    "The Earth orbits the sun once every 365 days.",
    "Mars is the fourth planet from the sun."
]

# Step 1: Generate document embeddings using OpenAI API
document_embeddings = []
for doc in documents:
    response = openai.Embedding.create(model="text-embedding-ada-002", input=doc)
    embedding = response['data'][0]['embedding']
    document_embeddings.append(embedding)

# Convert the embeddings to a numpy array
document_embeddings = np.array(document_embeddings).astype('float32')

# Step 2: Create an in-memory FAISS index
index = faiss.IndexFlatL2(len(document_embeddings[0]))  # L2 (Euclidean) distance
index.add(document_embeddings)  # Add document embeddings to the FAISS index

# Step 3: Example query
query = "How long does it take Earth to orbit the sun?"
query_embedding = openai.Embedding.create(model="text-embedding-ada-002", input=query)['data'][0]['embedding']
query_embedding = np.array(query_embedding).astype('float32').reshape(1, -1)

# Step 4: Search FAISS index for top 2 most similar documents
D, I = index.search(query_embedding, 2)  # D: distances, I: indices of results

# Step 5: Retrieve the most relevant documents
retrieved_docs = [documents[i] for i in I[0]]
print("Retrieved Documents:", retrieved_docs)

