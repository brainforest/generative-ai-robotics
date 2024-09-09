import os
from PyPDF2 import PdfReader
from gensim.utils import simple_preprocess
from gensim.models import Word2Vec
from annoy import AnnoyIndex
import numpy as np
from openai import OpenAI


# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        all_text = ""
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                all_text += text
    return all_text

# Function to split text into chunks
def split_text_into_chunks(text, chunk_size=1000, overlap=200):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

# Tokenize and preprocess texts
def preprocess(text):
    return simple_preprocess(text)

# Build Word2Vec model from preprocessed text
def build_word2vec_model(chunks):
    sentences = [preprocess(text) for text in chunks]
    model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, sg=0)
    return model

# Add vectors to Annoy index
def build_annoy_index(model, chunks):
    vector_size = model.vector_size
    index = AnnoyIndex(vector_size, 'angular')

    for i, text in enumerate(chunks):
        words = preprocess(text)
        word_vectors = [model.wv[word] for word in words if word in model.wv]
        if word_vectors:
            doc_vector = np.mean(word_vectors, axis=0)
            index.add_item(i, doc_vector)
    
    index.build(10)  # Build index with 10 trees
    return index

# Perform a similarity search
def find_similar(text, model, index, chunks, k=1):
    words = preprocess(text)
    word_vectors = [model.wv[word] for word in words if word in model.wv]
    if word_vectors:
        query_vector = np.mean(word_vectors, axis=0)
        nearest_neighbors = index.get_nns_by_vector(query_vector, k)
        return nearest_neighbors
    return []

# Main execution
def main(pdf_path):

    
    client = OpenAI()

    # Step 1: Extract text from PDF
    text = extract_text_from_pdf(pdf_path)
    
    # Step 2: Split text into chunks
    chunks = split_text_into_chunks(text)

    # Step 3: Build Word2Vec model
    model = build_word2vec_model(chunks)

    # Step 4: Build Annoy index
    annoy_index = build_annoy_index(model, chunks)

    # Step 5: Perform similarity search (Example)
    question = "what is the benefit of decentralized workflow engines in SAGA ?"
    query_text = question 
    nearest_neighbors = find_similar(query_text, model, annoy_index, chunks)

    context = ""
    print("Nearest neighbors (text indices):", nearest_neighbors)
    for i in nearest_neighbors:
        # print(f"Text Chunk {i}: {chunks[i]}\n")
        context += chunks[i] + " "
        
    print("You asked : ", question)
  
    prompt = ""
    if (len(context) > 10) :
         prompt = f"Based on this context : {context} you are IT Solution Architect and expert in this area. Please, answer this question : {question}"
    else:
         prompt = f"you are IT Solution Architect and expert in this area. Please, answer this question : {question}"

    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
       {"role": "user", "content": prompt}
    ])

    print("Open AI : " ,completion.choices[0].message.content)

# Example usage
pdf_file = "sample.pdf"  # Path to your PDF file
main(pdf_file)

