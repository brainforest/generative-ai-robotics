import spacy
from collections import defaultdict

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Sample text
text = """
    Apple Inc. is an American multinational technology company headquartered in Cupertino, California.
    It was founded by Steve Jobs, Steve Wozniak, and Ronald Wayne in 1976. Apple designs, develops, and sells consumer electronics, software, and online services.
    Its best-known products include the iPhone, iPad, Mac computers, and the Apple Watch. As of 2021, Tim Cook is the CEO of Apple.
"""

# Process text with SpaCy
doc = nlp(text)

# Dictionary to store entities
entities = defaultdict(list)

# Extract named entities (NER)
for ent in doc.ents:
    entities[ent.label_].append(ent.text)

# Print extracted entities
print("Named Entities:")
for entity_type, entity_list in entities.items():
    print(f"{entity_type}: {', '.join(set(entity_list))}")

# Summarization (simple extractive summarization)
def summarize(doc, ratio=0.3):
    sentences = list(doc.sents)
    n_sentences = int(len(sentences) * ratio)
    return " ".join([sent.text for sent in sentences[:n_sentences]])

# Summarize the text
summary = summarize(doc)
print("\nSummary:")
print(summary)

