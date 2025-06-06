import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet
from typing import Dict, List, Any

class NLPProcessor:
    def __init__(self):
        """Initialize the NLP processor with necessary models and configurations."""
        # Common word corrections for spell checking
        self.common_corrections = {
            'wat': 'what',
            'wht': 'what',
            'hw': 'how',
            'y': 'why',
            'cuz': 'because',
            'bc': 'because',
            'u': 'you',
            'r': 'are',
            'ur': 'your',
            'plz': 'please',
            'pls': 'please'
        }

    def process_message(self, message: str) -> Dict[str, Any]:
        """
        Process the input message through various NLP pipelines.
        
        Args:
            message: The input message from the user
            
        Returns:
            Dict containing processed message information
        """
        # Apply spell correction
        corrected_message = self._spell_correct(message)
        
        # Tokenize and tag
        tokens = word_tokenize(corrected_message)
        pos_tags = pos_tag(tokens)
        
        # Extract entities (simple named entity recognition)
        entities = self._extract_entities(pos_tags)
        
        # Determine intent
        intent = self._determine_intent(corrected_message)
        
        # Extract key phrases
        key_phrases = self._extract_key_phrases(pos_tags)
        
        return {
            'original': message,
            'corrected': corrected_message,
            'entities': entities,
            'intent': intent,
            'key_phrases': key_phrases,
            'tokens': tokens
        }

    def _spell_correct(self, text: str) -> str:
        """Apply spell correction to the input text."""
        words = text.lower().split()
        corrected_words = []
        
        for word in words:
            # Check common corrections first
            if word in self.common_corrections:
                corrected_words.append(self.common_corrections[word])
                continue
            
            # Keep the word as is if not in common corrections
            corrected_words.append(word)
        
        return ' '.join(corrected_words)

    def _determine_intent(self, text: str) -> str:
        """
        Determine the intent of the message using rule-based approach.
        """
        text = text.lower()
        first_word = text.split()[0] if text.split() else ''
        
        # Question detection
        if first_word in ['what', 'who', 'where', 'when', 'why', 'how']:
            return 'question'
        
        # Command detection
        if first_word in ['find', 'search', 'look', 'get', 'tell']:
            return 'command'
        
        # Greeting detection
        if any(word in text for word in ['hello', 'hi', 'hey', 'greetings']):
            return 'greeting'
        
        # Farewell detection
        if any(word in text for word in ['goodbye', 'bye', 'see you', 'farewell']):
            return 'farewell'
        
        return 'statement'

    def _extract_entities(self, pos_tags: List[tuple]) -> List[tuple]:
        """Extract named entities based on POS tags."""
        entities = []
        current_entity = []
        
        for word, tag in pos_tags:
            if tag.startswith(('NNP', 'NNPS')):  # Proper nouns
                current_entity.append(word)
            else:
                if current_entity:
                    entities.append((' '.join(current_entity), 'ENTITY'))
                    current_entity = []
        
        if current_entity:
            entities.append((' '.join(current_entity), 'ENTITY'))
        
        return entities

    def _extract_key_phrases(self, pos_tags: List[tuple]) -> List[str]:
        """Extract key phrases based on POS patterns."""
        key_phrases = []
        current_phrase = []
        
        for word, tag in pos_tags:
            if tag.startswith(('NN', 'JJ', 'VB')):  # Nouns, adjectives, verbs
                current_phrase.append(word)
            else:
                if current_phrase:
                    key_phrases.append(' '.join(current_phrase))
                    current_phrase = []
        
        if current_phrase:
            key_phrases.append(' '.join(current_phrase))
        
        return list(set(key_phrases))  # Remove duplicates 