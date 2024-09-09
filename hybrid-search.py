from annoy import AnnoyIndex
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Example data
documents = [
    "The theory of relativity is a scientific theory of the relationship between space and time.",
    "Quantum mechanics is a fundamental theory in physics that describes physical properties at the scale of atoms and subatomic particles.",
    "The standard model of particle physics describes the electromagnetic, weak, and strong nuclear forces."
]

# Create keyword index using CountVectorizer
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(documents)
keyword_index = {i: doc for i, doc in enumerate(documents)}

# Build vector index using Annoy
f = X.shape[1]
annoy_index = AnnoyIndex(f, 'angular')
for i, vector in enumerate(X.toarray()):
    annoy_index.add_item(i, vector)
annoy_index.build(10)  # 10 trees

# Search function
def hybrid_search(query, top_n=5):
    # Keyword search
    query_vector = vectorizer.transform([query]).toarray()
    cosine_similarities = cosine_similarity(query_vector, X).flatten()
    keyword_results = np.argsort(cosine_similarities)[::-1][:top_n]

    # Vector search
    query_annoy_vector = vectorizer.transform([query]).toarray().flatten()
    vector_results = annoy_index.get_nns_by_vector(query_annoy_vector, top_n)

    # Combine results
    combined_results = set(keyword_results).intersection(vector_results)
    
    return sorted(combined_results, key=lambda x: (cosine_similarities[x], vector_results.index(x)), reverse=True)

# Example query
query = "quantum theory"
print("You asked : ",query)
results = hybrid_search(query)
for result in results:
  print(keyword_index[result])

