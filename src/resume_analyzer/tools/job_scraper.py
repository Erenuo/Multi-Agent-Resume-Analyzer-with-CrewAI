from crewai.tools import tool
from bs4 import BeautifulSoup
import requests


@tool("Job URL Scraper")
def scrape_job_url(url: str) -> str:
    """
    Scrape and extract job description content from a URL.
    """
    try:
        url = url.strip().strip('"').strip("'")
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            element.decompose()
        
        main_content = None
        selectors = [
            'article',
            '[class*="job-description"]',
            '[class*="job-details"]',
            '[class*="description"]',
            '[id*="job-description"]',
            '[id*="job-details"]',
            'main',
            '[role="main"]',
        ]
        
        for selector in selectors:
            main_content = soup.select_one(selector)
            if main_content:
                break
        
        if not main_content:
            main_content = soup.body if soup.body else soup
        
        text = main_content.get_text(separator='\n', strip=True)
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        cleaned_text = '\n'.join(lines)
        
        if not cleaned_text:
            return "Error: Could not extract text content. The page might require JavaScript."
        
        max_chars = 10000
        if len(cleaned_text) > max_chars:
            cleaned_text = cleaned_text[:max_chars] + "\n\n[Content truncated due to length...]"
        
        return cleaned_text
        
    except requests.exceptions.Timeout:
        return f"Error: Request timed out for '{url}'."
    except requests.exceptions.ConnectionError:
        return f"Error: Could not connect to '{url}'."
    except requests.exceptions.HTTPError as e:
        return f"Error: HTTP error occurred: {str(e)}"
    except Exception as e:
        return f"Error scraping URL: {str(e)}"
