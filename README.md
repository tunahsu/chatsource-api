# Chatsource

This project offers APIs for managing chatbots with Retrieval-Augmented Generation (RAG), using OpenAI’s LLMs and embeddings. Users can create, train, and query chatbots, with support for document-based training and multi-user management.

## Features

- **User Authentication**: User-based authentication with support for managing multiple chatbots per user.
- **Chatbot Creation**: Users can create chatbots by specifying their parameters such as language model, temperature, and instructions.
- **Document-Based Training**: Chatbots can be trained with documents provided by the user. Each document is linked to a chatbot and is used for enhancing its capabilities.
- **Custom Query Engine**: Users can query their chatbots, and the system will generate responses using OpenAI's models based on the trained documents.
- **Embedding Support**: The system uses OpenAI's embedding model for processing documents and queries.
- **Vector Indexing**: A vector store is used to enhance the query engine's efficiency in generating responses.

## Tech Stack

- **FastAPI**: Fast and modern web framework for building APIs with Python.
- **OpenAI API**: Utilizes OpenAI's models for both generating responses and embedding content.
- **LlamaIndex**: Used to create and manage a vector store index for efficient document querying and retrieval.

## Installation

1. Clone the repository:
   ```bash
    git clone https://github.com/tunahsu/chatsource-api.git
    cd chatsource-api
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables: Create a .env file in the project root and add the necessary environment variables (e.g., OpenAI API key, database connection).

4. Run the development server:
    ```bash
    python main.py
    ```