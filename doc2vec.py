from gensim.models.doc2vec import Doc2Vec, TaggedDocument

# Sample documents (titles and content)
documents = [
    "Machine learning is fascinating.",
    "Artificial intelligence is the future.",
    "I love reading about AI and machine learning.",
    "Data science involves statistics and coding.",
    "Python is a versatile programming language.",
    "AI and machine learning are transforming industries.",
]

# Preprocess the documents: tokenize by splitting words and tag each one with a unique ID
tagged_data = [TaggedDocument(words=doc.lower().split(), tags=[str(i)]) for i, doc in enumerate(documents)]

# Initialize and train the Doc2Vec model
model = Doc2Vec(vector_size=50, window=2, min_count=1, workers=4, epochs=100)
model.build_vocab(tagged_data)
model.train(tagged_data, total_examples=model.corpus_count, epochs=model.epochs)

# Example: Search for documents similar to a given query
query = "I like machine learning and AI"
query_vector = model.infer_vector(query.lower().split())

# Find the most similar documents
similar_docs = model.dv.most_similar([query_vector], topn=3)

# Print the results
print("Query:", query)
print("\nMost similar documents:")
for idx, similarity in similar_docs:
    print(f"Document {idx}: {documents[int(idx)]} (similarity: {similarity:.2f})")
