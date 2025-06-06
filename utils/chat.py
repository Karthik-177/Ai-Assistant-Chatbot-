import requests
import os
from typing import Dict, List, Any
import uuid
import json
from datetime import datetime
import re

class ChatManager:
    def __init__(self):
        """Initialize the chat manager with necessary configurations."""
        self.conversations = {}
        self.max_context_length = 10  # Maximum number of messages to keep in context
        self.ollama_api_url = "http://localhost:11434/api/chat"
        self.model = "deepseek-r1:1.5b"

    def generate_response(self, processed_message: Dict[str, Any], 
                         context: List[Dict[str, str]], 
                         web_info: Dict[str, Any]) -> str:
        """
        Generate a response using the processed message, context, and web information.
        
        Args:
            processed_message: The processed user message
            context: Previous conversation context
            web_info: Information retrieved from web sources
            
        Returns:
            Generated response string
        """
        # Prepare the messages for the API
        messages = self._prepare_messages(processed_message, context, web_info)
        
        try:
            # Generate response using Ollama
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            }
            
            response = requests.post(self.ollama_api_url, json=payload)
            if response.status_code == 200:
                content = response.json()['message']['content']
                # Clean up the response
                content = self._clean_response(content)
                return content
            else:
                print(f"Error from Ollama API: {response.text}")
                return "I apologize, but I'm having trouble generating a response right now. Please try again."
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I apologize, but I'm having trouble generating a response right now. Please try again."

    def _clean_response(self, response: str) -> str:
        """Clean up the model's response by removing thinking process and formatting."""
        # Remove thinking process enclosed in <think> tags
        response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
        
        # Remove any remaining XML-like tags
        response = re.sub(r'<[^>]+>', '', response)
        
        # Clean up multiple newlines and spaces
        response = re.sub(r'\n\s*\n', '\n\n', response)
        response = re.sub(r' +', ' ', response)
        
        return response.strip()

    def _prepare_messages(self, processed_message: Dict[str, Any], 
                         context: List[Dict[str, str]], 
                         web_info: Dict[str, Any]) -> List[Dict[str, str]]:
        """Prepare messages for the Ollama API."""
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful AI assistant with access to real-time web information. "
                    "Provide clear, concise, and accurate responses. Do not show your thinking process. "
                    "If using web information, cite sources briefly. Keep responses focused and to the point. "
                    "Use natural, conversational language but maintain professionalism."
                )
            }
        ]
        
        # Add context messages
        for msg in context:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Add web information context
        web_context = self._format_web_info(web_info)
        if web_context:
            messages.append({
                "role": "system",
                "content": f"Web search results:\n{web_context}"
            })
        
        # Add the current message
        messages.append({
            "role": "user",
            "content": processed_message["corrected"]
        })
        
        return messages

    def get_context(self, conversation_id: str) -> List[Dict[str, str]]:
        """Retrieve conversation context for the given ID."""
        if not conversation_id or conversation_id not in self.conversations:
            return []
        return self.conversations[conversation_id][-self.max_context_length:]

    def update_history(self, user_message: str, bot_response: str, 
                      conversation_id: str = None) -> str:
        """
        Update conversation history and return conversation ID.
        
        Args:
            user_message: The user's message
            bot_response: The bot's response
            conversation_id: Optional conversation ID
            
        Returns:
            Conversation ID (new or existing)
        """
        if not conversation_id:
            conversation_id = str(uuid.uuid4())
            self.conversations[conversation_id] = []
            
        self.conversations[conversation_id].append({
            'role': 'user',
            'content': user_message,
            'timestamp': datetime.now().isoformat()
        })
        
        self.conversations[conversation_id].append({
            'role': 'assistant',
            'content': bot_response,
            'timestamp': datetime.now().isoformat()
        })
        
        return conversation_id

    def _format_web_info(self, web_info: Dict[str, Any]) -> str:
        """Format web information into a readable context string."""
        context_parts = []
        
        # Add Wikipedia information
        if web_info.get('wikipedia'):
            wiki_info = web_info['wikipedia']
            context_parts.append(
                f"Wikipedia ({wiki_info['title']}):\n{wiki_info['summary']}\n"
            )
        
        return "\n".join(context_parts) 