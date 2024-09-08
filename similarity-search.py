from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
from annoy import AnnoyIndex
import numpy as np

# Sample scientific texts
texts = [
    "The theory of relativity is a scientific theory of the relationship between space and time.",
    "Quantum mechanics is a fundamental theory in physics that provides a description of physical properties at the scale of atoms and subatomic particles.",
    "The standard model of particle physics is a theory concerning the electromagnetic, weak, and strong nuclear forces.",
    "Neuroscience is the scientific study of the nervous system, aiming to understand how the brain and its components work.",
    "Genetics is a branch of biology concerned with the study of genes, genetic variation, and heredity in organisms."
]

# Tokenize and preprocess texts
def preprocess(text):
    return simple_preprocess(text)

# Build Word2Vec model
sentences = [preprocess(text) for text in texts]
model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, sg=0)

# Create Annoy index
vector_size = model.vector_size
index = AnnoyIndex(vector_size, 'angular')

# Add vectors to Annoy index
for i, text in enumerate(texts):
    # Create a vector for the whole document by averaging word vectors
    words = preprocess(text)
    word_vectors = [model.wv[word] for word in words if word in model.wv]
    if word_vectors:
        doc_vector = np.mean(word_vectors, axis=0)
        index.add_item(i, doc_vector)

index.build(10)  # Build index with 10 trees

# Perform a similarity search
def find_similar(text, k=2):
    words = preprocess(text)
    word_vectors = [model.wv[word] for word in words if word in model.wv]
    if word_vectors:
        query_vector = np.mean(word_vectors, axis=0)
        return index.get_nns_by_vector(query_vector, k)

# Example search
query_text = "Quantum physics and particle theory"
nearest_neighbors = find_similar(query_text)

print("Nearest neighbors:", nearest_neighbors)
for i in nearest_neighbors:
    print(f"Text: {texts[i]}")
