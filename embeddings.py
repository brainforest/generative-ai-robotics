import numpy as np
from annoy import AnnoyIndex
from openai import OpenAI
client = OpenAI()

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
    response = client.embeddings.create(input=[doc],  model='text-embedding-3-small')
    embedding = response.data[0].embedding  
    document_embeddings.append(embedding)

# Convert the embeddings to a numpy array
document_embeddings = np.array(document_embeddings).astype('float32')

# Step 2: Create an Annoy index (we use Euclidean distance here, denoted by 2)
dimension = len(document_embeddings[0])  # dimensionality of the embeddings
annoy_index = AnnoyIndex(dimension, 'euclidean')

# Add document embeddings to the Annoy index
for i, embedding in enumerate(document_embeddings):
    annoy_index.add_item(i, embedding)

# Build the Annoy index (10 trees for faster search, can be adjusted)
annoy_index.build(10)

# Step 3: Example query
query = "How long does it take Earth to orbit the sun?"
query_embedding = client.embeddings.create(model="text-embedding-ada-002", input=query).data[0].embedding
query_embedding = np.array(query_embedding).astype('float32')

# Step 4: Search Annoy index for top 2 most similar documents
# The search_k parameter controls the tradeoff between accuracy and speed
top_n = 2
similar_doc_ids = annoy_index.get_nns_by_vector(query_embedding, top_n, search_k=-1, include_distances=True)
indices, distances = similar_doc_ids[0], similar_doc_ids[1]

# Step 5: Retrieve the most relevant documents
retrieved_docs = [documents[i] for i in indices]
print("Retrieved Documents:", retrieved_docs)

