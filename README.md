# Intelligent Web-Integrated AI Chatbot

A sophisticated AI chatbot that combines real-time web information retrieval, natural language processing, and a modern user interface to provide intelligent responses across a wide range of topics.

## Features

- Modern, responsive web interface
- Real-time web information retrieval
- Advanced NLP capabilities (spell correction, context understanding)
- Multi-turn conversation support
- Integration with multiple APIs (Google Search, Wikipedia, OpenAI)
- Voice input support (optional)
- Chat history logging
- Extensible architecture

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

## API Integration

The chatbot integrates with multiple APIs to provide comprehensive responses:
- OpenAI API for advanced language processing
- Google Search API for real-time information
- Wikipedia API for detailed knowledge
- Custom web scrapers for additional data

## Contributing

Feel free to submit issues and enhancement requests! 