"""
Custom tools for the Resume Analyzer Crew.

Tools:
    - parse_resume_file: Reads resume content from a local file path
    - scrape_job_url: Scrapes job description from a URL
"""

from resume_analyzer.tools.resume_parser import parse_resume_file
from resume_analyzer.tools.job_scraper import scrape_job_url

__all__ = ['parse_resume_file', 'scrape_job_url']
