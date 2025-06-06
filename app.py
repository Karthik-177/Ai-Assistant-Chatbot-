from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import json
from utils.nlp import NLPProcessor
from utils.web import WebSearcher
from utils.chat import ChatManager

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize components
nlp_processor = NLPProcessor()
web_searcher = WebSearcher()
chat_manager = ChatManager()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        conversation_id = data.get('conversation_id', None)

        # Process the message through NLP pipeline
        processed_message = nlp_processor.process_message(user_message)
        
        # Get conversation context
        context = chat_manager.get_context(conversation_id) if conversation_id else []
        
        # Search the web for relevant information
        web_info = web_searcher.search(processed_message)
        
        # Generate response using all available information
        response = chat_manager.generate_response(processed_message, context, web_info)
        
        # Update conversation history
        conversation_id = chat_manager.update_history(user_message, response, conversation_id)
        
        return jsonify({
            'response': response,
            'conversation_id': conversation_id,
            'sources': web_info.get('sources', [])
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/voice', methods=['POST'])
def voice():
    try:
        audio_data = request.files['audio']
        text = nlp_processor.speech_to_text(audio_data)
        return jsonify({'text': text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_ai_response(message, conversation_id=None):
    try:
        system_message = "Give extremely brief 1-2 sentence responses. Be direct and concise. No explanations."
        response = ollama.chat(
            model='deepseek:6b', # Using smaller model for faster responses
            messages=[
                {'role': 'system', 'content': system_message},
                {'role': 'user', 'content': message}
            ],
            options={
                'temperature': 0.7,
                'num_predict': 50  # Limit response length
            }
        )
        
        return {
            'response': response['message']['content'].strip(),
            'conversation_id': conversation_id
        }
    except Exception as e:
        print(f"Error getting AI response: {e}")
        return {
            'response': "Error: Please try again.",
            'conversation_id': None
        }

if __name__ == '__main__':
    app.run(debug=True) 