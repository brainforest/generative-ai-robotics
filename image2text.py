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
          "text": "You are IT solution architect and expert in software systems. Explain me in detail, What’s in this image?"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          }
        }
      ]
    }
  ]
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

result = response.json()

# What’s in this image?  
"""
The image shows a diagram illustrating two typical architectures for a business application that utilizes a workflow engine. 

1. **Workflow Engine as a Service**: 
   - It has two main components: "Your application" sits on top of a "Workflow engine."
  
2. **Embedded Workflow Engine (Library)**:
   - Here, "Your application" directly incorporates an embedded "Workflow engine" within its structure.

The image is labeled as "Figure 2-2" and is accompanied by the caption, "Typical architectures of a business application using a workflow engine."
"""

# You are IT solution architect and expert in software systems. Explain me in detail, What’s in this image? 

"""
The image illustrates two common architectural patterns for integrating a workflow engine within business applications. Here’s a detailed breakdown of each architecture:

### 1. Workflow Engine as a Service
- **Description**: In this architecture, the workflow engine operates as a separate service that your application interacts with. 
- **Components**:
  - **Your Application**: This represents the main software application that carries out business functions.
  - **Workflow Engine**: A standalone service or module responsible for managing workflow processes, tasks, and business rules. It may be deployed in the cloud or on a local server, providing APIs for your application to interact with it.
  
- **Advantages**:
  - **Scalability**: As a separate service, the workflow engine can scale independently based on demand.
  - **Maintainability**: Updates and maintenance can be performed on the workflow engine without impacting the core application.
  - **Interoperability**: Multiple applications can leverage the same workflow engine, promoting reusability.

- **Use Cases**: Suitable for applications that need dynamic workflow management and where workflows need to be consistently applied across different applications.

### 2. Embedded Workflow Engine (Library)
- **Description**: This architecture involves integrating the workflow engine directly into your application as a library or component.
- **Components**:
  - **Your Application**: Similar to the previous model, this is the main application, but it now includes the workflow engine as an internal library.
  - **Workflow Engine**: Embedded within the application, this engine is tightly coupled to the application code.

- **Advantages**:
  - **Performance**: Direct integration can lead to better performance due to reduced latency in invoking workflows.
  - **Simplicity**: For smaller applications, having everything in one package can simplify deployment and management.
  - **Control**: Updates to the workflow can be controlled and deployed along with the application.

- **Use Cases**: Best for smaller or simpler applications where the overhead of managing a separate service outweighs the benefits, or when tight integration is necessary.

### Conclusion
The choice between these two architectures largely depends on the specific needs of the application, including scalability, performance, and maintainability considerations. Understanding these patterns helps in designing software systems that effectively integrate workflow management capabilities.

"""

# Extracting just the 'content' field
content = result['choices'][0]['message']['content']
print(content)

