import requests
import wikipediaapi
from typing import Dict, List, Any
import json
from bs4 import BeautifulSoup
import urllib.parse

class WebSearcher:
    def __init__(self):
        """Initialize the web searcher with necessary APIs."""
        self.wiki = wikipediaapi.Wikipedia(
            language='en',
            extract_format=wikipediaapi.ExtractFormat.WIKI,
            user_agent='AIAssistantBot/1.0 (your-email@example.com)'  # Replace with your contact info
        )
        self.search_results_limit = 3

    def search(self, query: str) -> Dict[str, Any]:
        """
        Perform a web search using Wikipedia.
        
        Args:
            query: The search query
            
        Returns:
            Dict containing search results and sources
        """
        # Wikipedia search
        wiki_results = self._wiki_search(query)
        
        # For now, we'll return only Wikipedia results
        # Later we can add more search providers if needed
        return {
            'wikipedia': wiki_results,
            'query': query
        }

    def _wiki_search(self, query: str) -> Dict[str, str]:
        """Perform a Wikipedia search."""
        try:
            page = self.wiki.page(query)
            if page.exists():
                return {
                    'title': page.title,
                    'summary': page.summary[:500],  # Get first 500 characters of summary
                    'url': page.fullurl
                }
        except Exception as e:
            print(f"Error in Wikipedia search: {e}")
        
        return {}

    def _extract_title_from_url(self, url: str) -> str:
        """Extract a readable title from a URL."""
        try:
            parsed = urllib.parse.urlparse(url)
            # Get domain name
            domain = parsed.netloc.replace('www.', '')
            # Get path without extension
            path = parsed.path.rstrip('/').split('/')[-1].replace('-', ' ').replace('_', ' ')
            if path:
                return f"{path.title()} - {domain}"
            return domain
        except Exception as e:
            print(f"Error extracting title from URL: {e}")
            return url

    def _extract_snippet(self, html_content: str, max_length: int = 200) -> str:
        """Extract a relevant text snippet from HTML content."""
        # This is a simple implementation - could be improved with BeautifulSoup
        # and better text extraction
        try:
            # Remove HTML tags (very basic implementation)
            text = html_content.split('<body')[1].split('</body>')[0]
            text = ' '.join(text.split())
            
            # Get a snippet
            if len(text) > max_length:
                text = text[:max_length] + '...'
            
            return text
        except:
            return "" 