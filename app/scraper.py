import requests
import logging
from bs4 import BeautifulSoup
import json
import time
import os
import re
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class MediumScraper:
    """
    A class for scraping content from Medium articles.
    """

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.timeout = 10
        self.max_retries = 3

    def _fetch_page(self, url):
        """
        Fetch HTML content from the given URL with retries.
        
        Args:
            url (str): The URL to fetch
            
        Returns:
            str: HTML content of the page
        """
        for attempt in range(self.max_retries):
            try:
                response = requests.get(url, headers=self.headers, timeout=self.timeout)
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"Failed to fetch {url} after {self.max_retries} attempts")
                    raise

    def extract_article(self, url):
        """
        Extract content from a Medium article.
        
        Args:
            url (str): URL of the Medium article
            
        Returns:
            dict: Extracted article data including title, content, and metadata
        """        
        html_content = self._fetch_page(url)
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Create structured data dictionary
        article_data = {
            "url": url,
            "title": self._extract_title(soup),
            "author": self._extract_author(soup),
            "date": self._extract_date(soup),
            "content": self._extract_content(soup),
            "responses": [],
            "tags": self._extract_tags(soup),
            "reading_time": self._extract_reading_time(soup)
        }
        article_data["responses"] = self._extract_comments_from_content(article_data["content"])
        
        return article_data
    def _extract_comments_from_content(self, content):
        comments = []
        for section in content[:]: 
            if isinstance(section, dict) and section.get("type") == "section":
                title = section.get("title", "")
                if title and title.startswith("Top comments"):
                    for item in section.get("content", []):
                        if isinstance(item, dict) and item.get("type") == "paragraph":
                            comments.append(item.get("text", ""))
                    
                    content.remove(section)
        
        return comments
    
    def _extract_title(self, soup):
        """Extract the article title"""
        title_tag = soup.find('h1')
        return title_tag.get_text().strip() if title_tag else "Title not found"

    def _extract_author(self, soup):
        """Extract the author information"""
        author_element = soup.find('a', {'class': 'crayons-link fw-bold'})
        if author_element:
            return author_element.get_text().strip()
        return "Author not found"

    def _extract_date(self, soup):
        """Extract the publication date"""
        date_element = soup.find('time', {'class': 'date-no-year'})
        if date_element:
            return date_element.get_text().strip()
        return "Date not found"

    def _extract_reading_time(self, soup):
        """Extract the estimated reading time"""
        reading_time = soup.find(text=re.compile('min read'))
        if reading_time:
            return reading_time.strip()
        return "Reading time not found"

    def _extract_content(self, soup):
        """
        Extract the article content with structure.
        
        Returns a list of dictionaries with section headers and paragraphs.
        """
        content = []
        article_element = soup.find('article')
        
        if not article_element:
            article_element = soup.find('section', class_=lambda c: c and 'section' in c)
            if not article_element:
                return [{"type": "error", "text": "Content could not be extracted"}]
        
        # Process all children of the article element
        current_section = {"type": "section", "title": None, "content": []}
        
        # Find all heading and paragraph elements in the article
        elements = article_element.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'figure', 'blockquote', 'pre'])
        
        for element in elements:
            # Skip the title (which we already extracted)
            if element.name == 'h1' and element.get_text().strip() == self._extract_title(soup):
                continue
                
            # Handle headings - create a new section
            if element.name in ['h1', 'h2', 'h3', 'h4']:
                # Save the previous section if it has content
                if current_section["content"]:
                    content.append(current_section)
                    
                # Start a new section
                current_section = {
                    "type": "section",
                    "title": element.get_text().strip(),
                    "content": []
                }
            
            # Handle paragraphs
            elif element.name == 'p':
                text = element.get_text().strip()
                if text:  # Only add non-empty paragraphs
                    current_section["content"].append({
                        "type": "paragraph",
                        "text": text
                    })
            
            # Handle figures/images
            elif element.name == 'figure':
                img = element.find('img')
                if img and img.get('src'):
                    current_section["content"].append({
                        "type": "image",
                        "src": img.get('src'),
                        "alt": img.get('alt', '')
                    })
            
            # Handle blockquotes
            elif element.name == 'blockquote':
                text = element.get_text().strip()
                if text:
                    current_section["content"].append({
                        "type": "quote",
                        "text": text
                    })
            
            # Handle code blocks
            elif element.name == 'pre':
                code = element.get_text().strip()
                if code:
                    current_section["content"].append({
                        "type": "code",
                        "text": code
                    })
        
        # Add the last section if it has content
        if current_section["content"]:
            content.append(current_section)
            
        return content
    
    def _extract_tags(self, soup):
        """Extract article tags"""
        tags = []
        tag_elements = soup.find_all('a', href=re.compile(r'/tag/'))
        
        for tag in tag_elements:
            tags.append(tag.get_text().strip())
            
        return tags

    def save_to_json(self, article_data, output_path):
        """
        Save the extracted article data to a JSON file.
        
        Args:
            article_data (dict): Extracted article data
            output_path (str): Path to save the JSON file
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(article_data, f, ensure_ascii=False, indent=2)
            
        logger.info(f"Article saved to {output_path}")
        return output_path

def main(url, output_path):
    """
    Main function to run the scraper directly.
    
    Args:
        url (str): URL of the Medium article to scrape
        output_path (str): Path to save the JSON output
    """
    scraper = MediumScraper()
    article_data = scraper.extract_article(url)
    scraper.save_to_json(article_data, output_path)
    return article_data

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python scraper.py <medium_article_url> [output_path]")
        sys.exit(1)
        
    url = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "output.json"
    main(url, output_path)