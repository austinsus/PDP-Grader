import trafilatura
import logging
import os
import re

def get_website_text_content(url: str) -> str:
    """
    This function takes a url and returns the main text content of the website.
    The text content is extracted using trafilatura and easier to understand.
    The results is not directly readable, better to be summarized by LLM before consume
    by the user.
    """
    try:
        # Send a request to the website
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            raise Exception("Failed to download content from the URL")
        
        text = trafilatura.extract(downloaded)
        if not text:
            raise Exception("Failed to extract text content from the website")
        
        logging.info(f"Successfully extracted {len(text)} characters from {url}")
        # Ensure the extractions directory exists
        os.makedirs("extracted_text", exist_ok=True)
        # Create a safe filename from the URL
        filename = re.sub(r'[^\w\-_.]', '_', url)[:100] + ".txt"
        filepath = os.path.join("extracted_text", filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(text)
        logging.info(f"Extracted text saved to {filepath}")
        return text
    
    except Exception as e:
        logging.error(f"Error scraping {url}: {e}")
        raise Exception(f"Unable to scrape website content: {str(e)}")
