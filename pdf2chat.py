from typing import Dict, Union
from pypdf import PdfReader
from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
import numpy as np
from annoy import AnnoyIndex
from openai import OpenAI
import warnings
from colorama import Fore, Style, init
import os
import argparse

# Initialize colorama
init(autoreset=True)

client = OpenAI()

def bookmark_dict(bookmarks, pdf, use_labels=True):
    """Convert the outline into a dictionary of titles and page numbers."""
    def parse_bookmarks(bookmarks):
        parsed = []
        for b in bookmarks:
            if isinstance(b, list):
                parsed.extend(parse_bookmarks(b))
            else:
                title = b.get('/Title', 'No Title')
                page_num = pdf.get_destination_page_number(b)
                if page_num is not None:
                    parsed.append((title, page_num))
        return parsed

    return parse_bookmarks(bookmarks)

def extract_text_between_pages(reader, start_page, end_page):
    # Initialize a list to store the text from the specified pages
    extracted_text = []
    
    # Loop through the pages between start_page and end_page (inclusive)
    for page_num in range(start_page - 1, end_page):  # Pages are 0-indexed
        page = reader.pages[page_num]
        extracted_text.append(page.extract_text())
    
    # Join the text and return
    return '\n'.join(extracted_text)


def extract_text_between_titles(text, title1, title2):
    # Find the start and end positions of the titles
    start_idx = text.find(title1)
    end_idx = text.find(title2)
    
    if start_idx == -1 or end_idx == -1:
        return "One or both titles not found."
    
    # Adjust the start index to the end of the first title
    start_idx += len(title1)
    
    if start_idx > end_idx:
        return "The first title appears after the second title."

    # Extract text between the two titles
    extracted_text = text[start_idx:end_idx].strip()
    
    return extracted_text.replace('\n', ' ').replace('\r', '').replace('- ','')

def get_next_title(bookmarks, current_title):
    """Return the next bookmark title and its page number given the current title."""
    current_title_lower = current_title.lower()

    # Find the index of the current_title
    for i, (title, page_num) in enumerate(bookmarks):
        if title.lower() == current_title_lower:
            # Return the next title and its page number if it exists
            if i + 1 < len(bookmarks):
                next_title, next_page_num = bookmarks[i + 1]
                return next_title, next_page_num + 1
            else:
                return None, None  # No next title, current_title is the last one

    return None, None  # current_title not found

def get_page_for_title(bookmarks, target_title):
    """Return the page number for a given bookmark title."""
    target_title_lower = target_title.lower()

    for title, page_num in bookmarks:
        if title.lower() == target_title_lower:
            return page_num + 1

    return None  # Title not found

# Tokenize and preprocess texts
def preprocess(text):
    return simple_preprocess(text)

# Perform a similarity search
def find_similar(text, model, index, k=10):
    words = preprocess(text)
    word_vectors = [model.wv[word] for word in words if word in model.wv]
    if word_vectors:
        query_vector = np.mean(word_vectors, axis=0)
        return index.get_nns_by_vector(query_vector, k)


# Main execution
def main(pdf_path):

    reader = PdfReader(pdf_path)

    print(f"Processing PDF file: {pdf_path}")
    
    bms = bookmark_dict(reader.outline, reader, use_labels=True)

    book = {}
    # Print just the titles
    for title, _ in bms:
        start_page = get_page_for_title(bms, title)
        if (start_page > 10 and start_page < 280):
                next_title, next_page = get_next_title(bms, title)

                if (next_page is not None and start_page <= next_page ): 
                    extracted_text = extract_text_between_pages(reader, start_page, next_page)
                    extracted_text = extract_text_between_titles(extracted_text, title, next_title)
                    if ("One or both titles not found" not in extracted_text):
                        book[title] = extracted_text 

    # Iterating over key-value pairs
    # for key, value in book.items():
    #      print(f"Key: {key}, Value: {value[:50]}")
 

    # Flatten the dictionary into lists for training
    titles = list(book.keys())
    contents = list(book.values())

    # Build Word2Vec model
    sentences = [preprocess(text) for text in contents]
    model = Word2Vec(sentences, vector_size=200, window=5, min_count=1, sg=0)

    # Create Annoy index
    vector_size = model.vector_size
    index = AnnoyIndex(vector_size, 'angular')

    # Add vectors to Annoy index
    for i, text in enumerate(contents):
      # Create a vector for the whole document by averaging word vectors
      words = preprocess(text)
      word_vectors = [model.wv[word] for word in words if word in model.wv]
      if word_vectors:
         doc_vector = np.mean(word_vectors, axis=0)
         index.add_item(i, doc_vector)

    index.build(10)  # Build index with 10 trees

    nearest_neighbors = find_similar("what is benefit of decentralized engines ?",model,index)

    print("Nearest neighbors:", nearest_neighbors)
    for i in nearest_neighbors:
        print(f"Text ====> {titles[i]} ***** {contents[i]} <====")


    # Continuous loop to get questions from user
    while True:
        question = input("Ask a question (or type 'exit' to quit): ")
        if question.lower() == 'exit':
            print("Exiting the program.")
            break

        # Perform similarity search based on the user's question
        query_text = question 
        nearest_neighbors = find_similar(query_text)

        context = ""
        for i in nearest_neighbors:
            context += contents[i] + " "

        if (len(context) > 10):
            print(Fore.GREEN + f"** context constructed! ** {len(context)}")

        print(Fore.YELLOW + "You asked: ", question)
        
        # Formulate the prompt for OpenAI
        prompt = ""
        if len(context) > 10:
            prompt = f"Based on this context: {context} you are an IT Solution Architect and expert in this area. Please, answer this question shortly : {question}"
        else:
            prompt = f"You are an IT Solution Architect and expert in this area. Please, answer this question shortly : {question}"

        # Send the prompt to OpenAI and get a response
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.2,
            messages=[
               {"role": "user", "content": prompt}
            ]
            
        )
        text =  completion.choices[0].message.content
        print(Fore.CYAN + "OpenAI's response: ", Fore.MAGENTA + text)
 
    
# Example usage
if __name__ == "__main__":
     parser = argparse.ArgumentParser(description="Process a PDF file.")
     parser.add_argument("pdf_file", help="Path to the PDF file")
                
     args = parser.parse_args()
     main(args.pdf_file)
 
    
