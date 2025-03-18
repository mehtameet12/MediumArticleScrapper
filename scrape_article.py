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

def scrape_article(url, output_path="raw_output.json"):
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

def process_article(input_path="raw_output.json", output_path="processed_output.json"):
    """
    Process the scraped article data using processor.py.
    
    Args:
        input_path (str): Path to the raw JSON file (output from scraper)
        output_path (str): Path to save the processed JSON file
    """
    try:
        logger.info(f"Starting to process article data from {input_path}")
        
        # Construct the command to run processor.py
        processor_script = os.path.join("app", "processor.py")
        command = f"python {processor_script} {input_path} {output_path}"
        
        # Execute the command
        os.system(command)
        logger.info(f"Successfully processed article and saved to {output_path}")
        
        return True
    except Exception as e:
        logger.error(f"Error processing article: {str(e)}", exc_info=True)
        return False

def summarize_article(input_path="processed_output.json"):
    """
    Summarize the article and analyze comments using summarization.py.
    
    Args:
        input_path (str): Path to the processed JSON file
    """
    try:
        logger.info(f"Starting to summarize article and analyze comments from {input_path}")
        
        # Construct the command to run summarization.py
        summarization_script = os.path.join("app", "summarization.py")
        command = f"python {summarization_script} {input_path}"
        
        # Execute the command
        os.system(command)
        logger.info(f"Successfully summarized article and analyzed comments.")
        
        return True
    except Exception as e:
        logger.error(f"Error summarizing article: {str(e)}", exc_info=True)
        return False

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "https://dev.to/qodo/introducing-qodo-gen-10-transform-your-workflow-with-agentic-ai-5a96"
    raw_output_path = sys.argv[2] if len(sys.argv) > 2 else "raw_output.json"
    processed_output_path = sys.argv[3] if len(sys.argv) > 3 else "processed_output.json"
    
    if not os.path.isabs(raw_output_path):
        raw_output_path = os.path.abspath(raw_output_path)
    if not os.path.isabs(processed_output_path):
        processed_output_path = os.path.abspath(processed_output_path)
    
    # Scrape the article
    success = scrape_article(url, raw_output_path)
    
    if success:
        print(f"Successfully scraped article and saved to {raw_output_path}")
        
        # Process the scraped article
        process_success = process_article(raw_output_path, processed_output_path)
        
        if process_success:
            print(f"Successfully processed article and saved to {processed_output_path}")
            
            # Summarize the article and analyze comments
            summarize_success = summarize_article(processed_output_path)
            
            if summarize_success:
                print("Successfully summarized article and analyzed comments.")
            else:
                print("Failed to summarize article.")
                sys.exit(1)
        else:
            print("Failed to process article.")
            sys.exit(1)
    else:
        print("Failed to scrape article.")
        sys.exit(1)