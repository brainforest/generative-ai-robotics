import base64
import requests
import os

# OpenAI API Key
api_key = os.getenv("OPENAI_API_KEY")

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = "image.png"

# Getting the base64 string
base64_image = encode_image(image_path)

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

payload = {
  "model": "gpt-4o-mini",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "What’s in this image?"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          }
        }
      ]
    }
  ],
  "max_tokens": 300
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

result = response.json()

"""response = {
    'id': 'chatcmpl-A7I8KtLOSG1UiEtywY9tI5y9AO9oL',
    'object': 'chat.completion',
    'created': 1726301364,
    'model': 'gpt-4o-mini-2024-07-18',
    'choices': [
        {
            'index': 0,
            'message': {
                'role': 'assistant',
                'content': 'The image depicts two typical architectures for a business application that uses a workflow engine. \n\n1. **Workflow Engine as a Service**: This architecture shows the application interacting with a workflow engine hosted as a service, indicating an external setup where the workflow engine operates independently from the application.\n\n2. **Embedded Workflow Engine (Library)**: This design illustrates the workflow engine being embedded directly within the application, suggesting that it functions as a library integrated into the application’s codebase.\n\nBoth architectures allow the application to manage workflows, but they differ in implementation and integration approaches.',
                'refusal': None
            },
            'logprobs': None,
            'finish_reason': 'stop'
        }
    ],
    'usage': {
        'prompt_tokens': 8513,
        'completion_tokens': 112,
        'total_tokens': 8625,
        'completion_tokens_details': {'reasoning_tokens': 0}
    },
    'system_fingerprint': 'fp_54e2f484be'
}"""

# Extracting just the 'content' field
content = result['choices'][0]['message']['content']
print(content)

