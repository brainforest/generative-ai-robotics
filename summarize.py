import spacy
import numpy as np
import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity

# Load SpaCy model for sentence tokenization and word vector representation
nlp = spacy.load('en_core_web_md')  # Use medium or large model for word vectors

# Function to tokenize text into sentences
def tokenize_sentences(text):
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents]

# Function to compute sentence similarity matrix
def sentence_similarity(sentences):
    # Compute the embeddings of each sentence
    sentence_embeddings = [nlp(sent).vector for sent in sentences]
    
    # Compute the cosine similarity matrix
    sim_matrix = np.zeros((len(sentences), len(sentences)))
    
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i != j:
                sim_matrix[i][j] = cosine_similarity(
                    sentence_embeddings[i].reshape(1, -1),
                    sentence_embeddings[j].reshape(1, -1)
                )[0][0]
    
    return sim_matrix

# Function to rank sentences using TextRank algorithm
def rank_sentences(sentences, similarity_matrix):
    # Create a graph and apply PageRank
    nx_graph = nx.from_numpy_array(similarity_matrix)
    scores = nx.pagerank(nx_graph)
    
    # Sort the sentences by score
    ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    return ranked_sentences

# Function to summarize the text by selecting top N ranked sentences
def summarize(text, num_sentences=3):
    sentences = tokenize_sentences(text)
    sim_matrix = sentence_similarity(sentences)
    ranked_sentences = rank_sentences(sentences, sim_matrix)
    
    # Extract the top N sentences as summary
    summary = " ".join([ranked_sentences[i][1] for i in range(num_sentences)])
    return summary

# Example usage:
text = """Alice was born in London. She met Bob in Paris, where they discussed quantum mechanics. 
Alice works for Google, while Bob is a researcher at MIT. Alice loves hiking in the mountains, 
while Bob enjoys surfing. They both have a keen interest in AI and robotics."""

# Summarize the text
summary = summarize(text, num_sentences=2)
print("Summary:", summary)

