from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
from annoy import AnnoyIndex
import numpy as np

# Sample information 

texts = [
    "Microservices are an architectural style where an application is developed as a collection of loosely coupled, independently deployable services.",
    "Each microservice typically manages its own database, allowing for more flexible data management and scaling.",
    "Microservices communicate with each other through well-defined APIs, such as RESTful services or message brokers.",
    "The primary benefit of microservices is improved scalability, allowing each component to be scaled independently based on demand.",
    "Microservices support technology diversity, meaning different services can use different programming languages and technologies.",
    "Fault isolation is a key advantage of microservices; failure in one service does not necessarily impact the entire system.",
    "Continuous deployment and integration are easier with microservices because each service can be deployed independently.",
    "Service discovery mechanisms, like Consul or Eureka, help locate and manage microservices dynamically.",
    "Load balancing distributes incoming requests across multiple instances of a microservice to ensure high availability and performance.",
    "DevOps practices are commonly used with microservices to streamline development, deployment, and operations.",
    "Polyglot persistence allows microservices to use various types of databases according to their specific needs, such as SQL and NoSQL databases.",
    "Resilience patterns like circuit breakers and retries are used in microservices to handle failures and ensure stability.",
    "An API Gateway serves as a single entry point for client requests, managing and routing them to the appropriate microservices.",
    "Centralized monitoring and logging are essential for tracking performance and debugging issues across multiple microservices.",
    "Security in microservices often involves implementing patterns such as OAuth for managing authentication and authorization.",
    "Handling data consistency in microservices often involves patterns like eventual consistency to ensure data integrity across services.",
    "Microservices are often designed using Domain-Driven Design (DDD) principles, focusing on business domains and bounded contexts.",
    "Clear and well-defined service contracts are crucial for maintaining interoperability and communication between microservices.",
    "Microservices can be deployed in various environments, including on-premises, in the cloud, or in hybrid setups.",
    "The API Gateway Pattern involves using a gateway to route client requests to appropriate microservices and manage cross-cutting concerns.",
    "The Circuit Breaker Pattern helps prevent cascading failures by stopping requests to a failing service and allowing it to recover.",
    "The Service Discovery Pattern allows services to dynamically find and communicate with each other without hardcoded network locations.",
    "The Aggregator Pattern collects and combines data from multiple microservices into a single response for the client.",
    "The Strangler Fig Pattern involves gradually replacing legacy systems with microservices by redirecting requests to the new system over time.",
    "The Saga Pattern manages distributed transactions across microservices by coordinating a series of local transactions to ensure data consistency.",
    "The Bulkhead Pattern isolates different parts of the system to prevent failures in one area from affecting others.",
    "The CQRS (Command Query Responsibility Segregation) Pattern separates the read and write operations of a service to optimize performance and scalability.",
    "The Event Sourcing Pattern involves persisting the state of a system as a sequence of events, which can be replayed to reconstruct the state.",
    "The Data Management Pattern helps handle data storage and retrieval strategies in a microservices architecture.",
    "The Sidecar Pattern involves deploying a secondary component alongside the primary microservice to handle cross-cutting concerns like logging and monitoring.",
    "The Proxy Pattern uses intermediaries to manage requests and responses between clients and microservices for various purposes, including security and load balancing.",
    "The Adapter Pattern allows microservices with incompatible interfaces to work together by providing a translation layer.",
    "The Decomposition Pattern involves breaking down a large monolithic application into smaller, manageable microservices.",
    "The Event-Driven Architecture Pattern uses events to trigger and communicate between microservices asynchronously, improving responsiveness and decoupling.",
    "The API Composition Pattern aggregates data from multiple microservices into a single response, often used in conjunction with API gateways.",
    "The Backend for Frontend (BFF) Pattern customizes backend services for specific frontend applications to optimize performance and user experience.",
    "The Feature Toggle Pattern enables or disables features of a microservice dynamically without redeploying the service.",
    "The Rate Limiting Pattern controls the number of requests a microservice can handle to prevent overload and ensure fair usage.",
    "The Circuit Breaker Pattern can be combined with fallback mechanisms to provide alternative responses when a service is unavailable.",
    "The Service Mesh Pattern provides a dedicated infrastructure layer for managing microservices communication, security, and monitoring.",
    "The Health Check Pattern involves regularly checking the status of microservices to ensure they are running correctly and are available.",
    "The Immutable Infrastructure Pattern uses versioned infrastructure components to ensure consistent deployment and reduce configuration drift.",
    "The Asynchronous Communication Pattern helps decouple microservices by using message queues or event streams for communication.",
    "The Throttling Pattern limits the rate of requests or operations to protect microservices from being overwhelmed and to ensure stability.",
    "The Proxy Pattern in microservices can also be used for implementing caching, security, and traffic management.",
    "The Failover Pattern ensures that if one instance of a microservice fails, another instance can take over to maintain availability.",
    "The Blue-Green Deployment Pattern allows deploying new versions of microservices with minimal downtime by switching between two environments.",
    "The Canary Release Pattern involves releasing new versions of microservices to a small subset of users before a full rollout to minimize risk.",
    "The Rollback Pattern provides mechanisms to revert to a previous version of a microservice in case of issues with the new version.",
    "The Service Decomposition Pattern breaks down complex services into smaller, more manageable microservices based on functionality or business capabilities.",
    "The Dependency Injection Pattern promotes loose coupling by injecting dependencies into microservices rather than having them directly create or manage dependencies.",
    "The Publish-Subscribe Pattern enables microservices to subscribe to and process events published by other services, promoting asynchronous communication.",
    "The Message Queue Pattern uses message queues to buffer and manage communication between microservices, helping handle high loads and ensure reliability.",
    "The Rate Limiting Pattern can be applied to APIs to prevent abuse and ensure fair use of microservices by limiting the number of requests.",
    "The Retry Pattern involves automatically retrying failed requests to microservices with configurable delay intervals to handle transient failures.",
    "The Timeout Pattern sets limits on the maximum amount of time a microservice should wait for a response from another service to avoid blocking.",
    "The Configuration Management Pattern centralizes configuration data for microservices, allowing dynamic updates and consistent configuration across services.",
    "The Security Pattern involves implementing measures such as encryption, authentication, and authorization to protect microservices and their data.",
    "The Monitoring Pattern provides tools and techniques for tracking the health, performance, and behavior of microservices in real-time.",
    "The Logging Pattern involves capturing and aggregating log data from microservices for debugging, analysis, and auditing purposes.",
    "The Data Replication Pattern involves synchronizing data across multiple instances of microservices to ensure consistency and high availability.",
    "The Fault Tolerance Pattern builds resilience into microservices by anticipating and handling failures gracefully, ensuring system stability.",
    "The Scalability Pattern involves designing microservices to handle increasing loads by adding more instances or resources as needed.",
    "The Service Orchestration Pattern coordinates the interactions between multiple microservices to achieve a specific business process or workflow.",
    "The Service Choreography Pattern allows microservices to coordinate their interactions autonomously, without a central orchestrator.",
    "The Event Streaming Pattern uses continuous streams of events to process and analyze data in real-time across microservices.",
    "The Aggregation Pattern involves combining data from multiple microservices into a single, cohesive result for the client or application.",
    "The Data Sharding Pattern divides data across multiple databases or microservices to distribute the load and improve performance.",
    "The Elasticity Pattern enables microservices to automatically scale resources up or down based on real-time demand or usage patterns.",
    "The Dependency Management Pattern addresses the challenge of managing and updating dependencies between microservices to ensure compatibility.",
    "The API Management Pattern provides tools and techniques for managing, monitoring, and securing APIs used by microservices.",
    "The Feature Flag Pattern allows developers to enable or disable features in microservices dynamically, facilitating controlled releases and testing.",
    "The Backpressure Pattern involves managing the flow of data between microservices to prevent overloading and ensure smooth processing.",
    "The State Management Pattern addresses the challenge of maintaining and synchronizing state across distributed microservices.",
    "The Health Monitoring Pattern involves tracking the health of microservices and automatically taking corrective actions if needed.",
    "The Dynamic Scaling Pattern adjusts the number of microservice instances based on real-time metrics and demand, optimizing resource usage.",
    "The Data Consistency Pattern ensures that data across microservices remains consistent and accurate, even in distributed environments.",
    "The Service Proxy Pattern uses intermediate proxies to handle cross-cutting concerns like authentication, logging, and routing in microservices.",
    "The Cross-Cutting Concerns Pattern manages aspects of microservices that are not specific to individual services but affect multiple services, such as security and logging.",
    "The Zero-Downtime Deployment Pattern ensures that microservices can be updated and deployed without causing interruptions to users.",
    "The Resource Isolation Pattern isolates resources used by different microservices to prevent interference and ensure optimal performance.",
    "The Retry-After Pattern provides a way for microservices to handle temporary failures by specifying when to retry failed requests.",
    "The Decomposition by Subdomain Pattern breaks down large microservices into smaller, more manageable services based on business subdomains.",
    "The Context Mapping Pattern defines relationships between different bounded contexts in microservices, facilitating integration and communication.",
    "The Change Data Capture Pattern captures and processes changes in data across microservices, ensuring consistency and synchronization.",
    "The Command Query Responsibility Segregation (CQRS) Pattern separates read and write operations to optimize performance and scalability.",
    "The Aggregated View Pattern provides a unified view of data from multiple microservices, often used for reporting and analysis.",
    "The Fault Injection Pattern tests the resilience of microservices by intentionally introducing faults or failures to observe system behavior.",
    "The Sidecar Proxy Pattern deploys a secondary component alongside a microservice to handle tasks like logging, monitoring, or security.",
    "The Data Transformation Pattern converts data formats or structures between different microservices to ensure compatibility and integration.",
    "The Rate Limiting and Throttling Pattern controls the rate of incoming requests to prevent service overload and ensure fair usage.",
    "The API Contract Pattern defines clear agreements and expectations between microservices regarding API interfaces and interactions.",
    "The Read-Write Separation Pattern separates data read and write operations to optimize performance and reduce contention.",
    "The Eventual Consistency Pattern ensures that distributed microservices reach a consistent state over time, even if not immediately.",
    "The Dependency Injection and Inversion of Control Pattern promotes loose coupling and flexibility by injecting dependencies into microservices.",
    "The Service Decomposition by Functionality Pattern breaks down services based on their specific functions or operations within the system.",
    "The Service Contract Testing Pattern ensures that microservices meet their defined contracts and interfaces through automated testing.",
    "The Service Resilience Pattern implements strategies like retries, fallbacks, and timeouts to enhance the reliability of microservices.",
    "The Blue-Green Deployment Pattern facilitates smooth and zero-downtime deployment by using two parallel environments for switching traffic.",
    "The Canary Release Pattern gradually rolls out new versions of microservices to a small subset of users before full deployment.",
    "The Backward Compatibility Pattern ensures that changes to microservices do not break compatibility with existing clients or services.",
    "The Rate Limiting Pattern controls the number of requests to a microservice to prevent abuse and maintain service quality.",
    "The Timeouts Pattern specifies limits on the duration of operations or requests to prevent microservices from hanging or becoming unresponsive.",
    "The Data Privacy Pattern implements measures to protect sensitive data in microservices, including encryption and access controls.",
    "The Service Choreography Pattern coordinates interactions between microservices without a central orchestrator, allowing autonomous behavior.",
    "The Service Orchestration Pattern manages and coordinates interactions between multiple microservices to achieve a business process.",
    "The Circuit Breaker Pattern prevents failures from propagating by detecting faults and stopping calls to failing services.",
    "The Proxy Pattern can be used to implement caching, security, and traffic management features in microservices.",
    "The Service Registry Pattern maintains a dynamic list of available microservices, enabling discovery and communication between them.",
    "The Event Source Pattern persists and replays events to reconstruct the state of a microservice or system.",
    "The Service Aggregation Pattern collects and combines responses from multiple microservices into a single response for the client.",
    "The Event-Driven Pattern uses events to trigger and communicate between microservices asynchronously, improving scalability and decoupling.",
    "The Hybrid Deployment Pattern combines multiple deployment models, such as on-premises and cloud, to meet specific requirements."
]



# Tokenize and preprocess texts
def preprocess(text):
    return simple_preprocess(text)

# Build Word2Vec model
sentences = [preprocess(text) for text in texts]
model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, sg=0)

# Create Annoy index
vector_size = model.vector_size
index = AnnoyIndex(vector_size, 'angular')

# Add vectors to Annoy index
for i, text in enumerate(texts):
    # Create a vector for the whole document by averaging word vectors
    words = preprocess(text)
    word_vectors = [model.wv[word] for word in words if word in model.wv]
    if word_vectors:
        doc_vector = np.mean(word_vectors, axis=0)
        index.add_item(i, doc_vector)

index.build(10)  # Build index with 10 trees

# Perform a similarity search
def find_similar(text, k=20):
    words = preprocess(text)
    word_vectors = [model.wv[word] for word in words if word in model.wv]
    if word_vectors:
        query_vector = np.mean(word_vectors, axis=0)
        return index.get_nns_by_vector(query_vector, k)

# Example search
query_text = "event-based microservice"
print("You search :", query_text)
nearest_neighbors = find_similar(query_text)

print("Nearest neighbors:", nearest_neighbors)
for i in nearest_neighbors:
    print(f"Text: {texts[i]}") 

