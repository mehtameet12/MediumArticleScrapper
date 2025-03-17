#!/usr/bin/env python3

import os
import logging
import sys
from app.scraper import MediumScraper

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def scrape_article(url, output_path="output.json"):
    """
    Scrape a Medium article and save it to a JSON file.
    
    Args:
        url (str): URL of the Medium article
        output_path (str): Path to save the output JSON
    """
    try:
        logger.info(f"Starting to scrape article: {url}")
        scraper = MediumScraper()
        
        article_data = scraper.extract_article(url)
        logger.info(f"Successfully extracted article: {article_data['title']}")
        
        scraper.save_to_json(article_data, output_path)
        logger.info(f"Article saved to {output_path}")
        
        return True
    except Exception as e:
        logger.error(f"Error scraping article: {str(e)}", exc_info=True)
        return False

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "https://medium.com/electronic-life/ai-music-style-can-there-be-too-much-culture-6e1f5480794a"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "output.json"
    
    if not os.path.isabs(output_path):
        output_path = os.path.abspath(output_path)
    
    success = scrape_article(url, output_path)
    
    if success:
        print(f"Successfully scraped article and saved to {output_path}")
    else:
        print("Failed to scrape article.")
        sys.exit(1)