from openai import OpenAI
import json
import os

client = OpenAI()

max_history_length = 100
# File to store conversation history
history_file = "conversation_history.json"

# Function to load conversation history from a file
def load_history():
    if os.path.exists(history_file):
        with open(history_file, 'r',encoding='utf-8') as file:
            history = json.load(file)
            # Keep only the last 100 messages
            if len(history) > max_history_length:
                history = history[-max_history_length:]
            return history
    return [{"role": "system", "content": "Merhaba, sen harika bir yardımcısın, Lütfen, kısa ve öz cevaplar ver."}]

# Function to save conversation history to a file
def save_history(history):
    with open(history_file, 'w', encoding='utf-8') as file:
        json.dump(history, file, ensure_ascii=False, indent=4)


# Initialize the conversation history by loading from file
conversation_history = load_history()

# Function to add a message to the conversation history
def add_to_history(role, content):
    conversation_history.append({"role": role, "content": content})
    # Keep only the last 100 messages
    if len(conversation_history) > max_history_length:
        conversation_history.pop(0)
    # Save history to file after each addition
    save_history(conversation_history)

# Function to interact with OpenAI
def chat_with_openai(user_input):
    add_to_history("user", user_input)
    
    # Generate a response from OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation_history
    )
    
    # Extract the assistant's message and add it to the history
    assistant_message = response.choices[0].message.content 
    add_to_history("assistant", assistant_message)
    
    return assistant_message


# Continuous conversation loop
while True:
    user_input = input("You: ")  # Get input from the user
    
    if user_input.lower() in ["exit", "quit", "stop"]:
        print("Ending conversation.")
        break
    
    response = chat_with_openai(user_input)
    
    # Print the assistant's response
    print(f"Assistant: {response}")

