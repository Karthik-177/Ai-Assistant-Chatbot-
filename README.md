# Intelligent Web-Integrated AI Chatbot

This project is an AI chatbot designed to provide intelligent and context-aware responses by integrating real-time web information retrieval, advanced natural language processing, and multi-turn conversation management.

It leverages a modular architecture combining NLP processing, web search via Wikipedia, and AI response generation using the Ollama "deepseek-r1:1.5b" model to deliver accurate, contextually relevant, and conversational replies through a modern web interface.

## Features

- Modern, responsive web interface
- Real-time web information retrieval using Wikipedia API
- Advanced NLP capabilities (spell correction, context understanding)
- Multi-turn conversation support with conversation history
- Integration with Ollama API for advanced language processing
- Voice input support via audio transcription
- Chat history logging and management
- Extensible and modular architecture

## Setup Instructions

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```
5. Run the application:
   ```bash
   python app.py
   ```
6. Open http://localhost:5000 in your browser

## Project Structure

```
.
├── app.py              # Flask application entry point
├── static/            # Static files (CSS, JS, images)
├── templates/         # HTML templates
├── utils/            # Utility functions
│   ├── nlp.py       # NLP processing functions
│   ├── web.py       # Web scraping and API integration
│   └── chat.py      # Chat processing logic
└── requirements.txt  # Project dependencies
```

## Code Overview

The application is built using Flask and consists of several key components:

- **NLPProcessor**: Handles natural language processing tasks such as message processing and speech-to-text conversion.
- **WebSearcher**: Performs real-time web searches to retrieve relevant information to enhance chatbot responses.
- **ChatManager**: Manages conversation context, generates responses based on processed messages, context, and web search results, and maintains chat history.

### Model

The chatbot uses the Ollama API with the "deepseek-r1:1.5b" model for generating AI responses, providing efficient and contextually relevant replies.

The application also uses `flask_cors` to enable Cross-Origin Resource Sharing and `python-dotenv` to manage environment variables.

## API Endpoints

- `GET /`  
  Serves the main chat interface.

- `POST /api/chat`  
  Accepts a JSON payload with:
  ```json
  {
    "message": "User's message",
    "conversation_id": "Optional conversation ID"
  }
  ```
  Returns a JSON response with:
  ```json
  {
    "response": "Chatbot's reply",
    "conversation_id": "Updated conversation ID",
    "sources": ["List of web information sources"]
  }
  ```

- `POST /api/voice`  
  Accepts audio file data and returns the transcribed text:
  ```json
  {
    "text": "Transcribed speech text"
  }
  ```

└── requirements.txt  # Project dependencies

## API Integration

The chatbot integrates with multiple APIs to provide comprehensive responses:
- Ollama API for advanced language processing
- Wikipedia API for detailed knowledge

## Contributing

Feel free to submit issues and enhancement requests! 