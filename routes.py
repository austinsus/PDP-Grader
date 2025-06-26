import logging
from flask import render_template, request, flash, redirect, url_for
from urllib.parse import urlparse
from app import app
from web_scraper import get_website_text_content
from openai_analyzer import analyze_website_content

@app.route('/')
def index():
    """Main page with URL input form"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Handle URL submission and analysis"""
    url = request.form.get('url', '').strip()
    
    # Validate URL
    if not url:
        flash('Please enter a URL', 'error')
        return redirect(url_for('index'))
    
    # Add protocol if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Parse and validate URL
    try:
        parsed = urlparse(url)
        if not parsed.netloc:
            flash('Please enter a valid URL', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        logging.error(f"URL parsing error: {e}")
        flash('Please enter a valid URL', 'error')
        return redirect(url_for('index'))
    
    try:
        # Scrape website content
        logging.info(f"Scraping content from: {url}")
        content = get_website_text_content(url)
        
        if not content or len(content.strip()) < 50:
            flash('Unable to extract sufficient content from the website. Please check the URL and try again.', 'error')
            return redirect(url_for('index'))
        
        # Analyze content with ChatGPT
        logging.info("Analyzing content with ChatGPT")
        analysis = analyze_website_content(content, url)
        
        return render_template('analysis.html', 
                             url=url, 
                             analysis=analysis)
        
    except Exception as e:
        logging.error(f"Analysis error: {e}")
        flash(f'Error analyzing website: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('index.html')

@app.errorhandler(500)
def internal_error(error):
    flash('An internal error occurred. Please try again.', 'error')
    return render_template('index.html')
