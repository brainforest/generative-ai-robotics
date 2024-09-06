import wikipediaapi
import json
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI()

# Wikipedia API setup with custom User-Agent
wiki_wiki = wikipediaapi.Wikipedia(user_agent='MyBot/1.0 (https://mywebsite.com; myemail@example.com)')

# Generate a natural language query response using OpenAI Chat API
def ask_openai(question, context):
    # Combine question with Neo4j data context

    full_prompt = f"Given the following information:\n{context}\n\nAnswer the following question: {question}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Specify the chat model
        messages=[
            {"role": "user", "content": full_prompt}
        ]
    )
    return response.choices[0].message.content

# Function to fetch a Wikipedia page
def get_wikipedia_page(title):
    page = wiki_wiki.page(title)
    if page.exists():
        return page
    else:
        print(f"{title} does not exist.")
        return None

# Function to extract page summary and links
def extract_wikipedia_info(page):
    # Extract summary and links for knowledge graph
    data = {
        "title": page.title,
        "summary": page.summary,
        "links": []
    }

    # Add linked articles (up to 5 for simplicity)
    for link_title in list(page.links.keys())[:5]:
        linked_page = wiki_wiki.page(link_title)
        if linked_page.exists():
            data["links"].append({
                "title": linked_page.title,
                "summary": linked_page.summary
            })
    return data

# Main function to generate graph-like JSON structure from Wikipedia
def generate_graph_json(topic):
    page = get_wikipedia_page(topic)
    if page:
        graph_data = extract_wikipedia_info(page)
        return graph_data
    else:
        return {"error": "Topic not found on Wikipedia"}


# Example usage
if __name__ == "__main__":
    topic = "Compensating transaction"  # Change to any topic you want
    result = generate_graph_json(topic)
    print(json.dumps(result, indent=4))

     # Ask OpenAI a question, passing Neo4j results as context

    user_question = "What are the methods of achiving data consistency in microservice architectures ?"
    print(f"You Asked: {user_question}")
    answer = ask_openai(user_question, result)
    print(f"OpenAI Answer: {answer}")


