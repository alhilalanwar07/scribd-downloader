#!/usr/bin/env python3
"""
Scribd Downloader
A tool to download documents from Scribd

Author: Assistant
Version: 1.0
"""

import requests
import os
import re
import json
import time
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import base64
from PIL import Image
import io

class ScribdDownloader:
    def __init__(self, headless=True):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.headless = headless
        self.driver = None
        
    def setup_driver(self):
        """Setup Chrome WebDriver"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            return True
        except Exception as e:
            print(f"Error setting up Chrome driver: {e}")
            print("Please make sure ChromeDriver is installed and in PATH")
            return False
    
    def extract_document_info(self, url):
        """Extract document information from Scribd URL"""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title_elem = soup.find('h1', class_='document_title') or soup.find('title')
            title = title_elem.get_text().strip() if title_elem else 'Unknown Document'
            
            # Clean title for filename
            title = re.sub(r'[<>:"/\\|?*]', '_', title)
            
            # Extract document ID from URL
            doc_id_match = re.search(r'/document/(\d+)/', url)
            doc_id = doc_id_match.group(1) if doc_id_match else None
            
            return {
                'title': title,
                'doc_id': doc_id,
                'url': url
            }
            
        except Exception as e:
            print(f"Error extracting document info: {e}")
            return None
    
    def download_with_selenium(self, url, output_dir='downloads'):
        """Download document using Selenium (for dynamic content)"""
        if not self.setup_driver():
            return False
            
        try:
            print(f"Loading page: {url}")
            self.driver.get(url)
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Extract document info
            doc_info = self.extract_document_info(url)
            if not doc_info:
                print("Could not extract document information")
                return False
                
            print(f"Document: {doc_info['title']}")
            
            # Create output directory
            os.makedirs(output_dir, exist_ok=True)
            
            # Try different methods to download
            success = False
            
            # Method 1: Look for download button
            success = self._try_download_button(doc_info, output_dir)
            
            # Method 2: Screenshot pages if download button not available
            if not success:
                success = self._screenshot_pages(doc_info, output_dir)
            
            # Method 3: Extract text content
            if not success:
                success = self._extract_text_content(doc_info, output_dir)
            
            return success
            
        except Exception as e:
            print(f"Error during download: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
    
    def _try_download_button(self, doc_info, output_dir):
        """Try to find and click download button"""
        try:
            # Look for various download button selectors
            download_selectors = [
                'button[data-testid="download-button"]',
                '.download_button',
                'button:contains("Download")',
                'a:contains("Download")',
                '[aria-label*="download"]'
            ]
            
            for selector in download_selectors:
                try:
                    download_btn = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    download_btn.click()
                    print("Download initiated...")
                    time.sleep(5)  # Wait for download
                    return True
                except (TimeoutException, NoSuchElementException):
                    continue
                    
            return False
            
        except Exception as e:
            print(f"Error trying download button: {e}")
            return False
    
    def _screenshot_pages(self, doc_info, output_dir):
        """Take screenshots of document pages"""
        try:
            print("Attempting to capture document pages...")
            
            # Look for page elements
            page_selectors = [
                '.page',
                '.document_page',
                '[data-page]',
                '.text_layer'
            ]
            
            pages_found = False
            for selector in page_selectors:
                try:
                    pages = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if pages:
                        pages_found = True
                        break
                except:
                    continue
            
            if not pages_found:
                print("No document pages found for screenshot")
                return False
            
            # Create directory for this document
            doc_dir = os.path.join(output_dir, doc_info['title'])
            os.makedirs(doc_dir, exist_ok=True)
            
            # Screenshot each page
            for i, page in enumerate(pages[:10]):  # Limit to first 10 pages
                try:
                    # Scroll page into view
                    self.driver.execute_script("arguments[0].scrollIntoView();", page)
                    time.sleep(1)
                    
                    # Take screenshot
                    screenshot_path = os.path.join(doc_dir, f"page_{i+1}.png")
                    page.screenshot(screenshot_path)
                    print(f"Saved page {i+1}")
                    
                except Exception as e:
                    print(f"Error capturing page {i+1}: {e}")
                    continue
            
            print(f"Screenshots saved to: {doc_dir}")
            return True
            
        except Exception as e:
            print(f"Error taking screenshots: {e}")
            return False
    
    def _extract_text_content(self, doc_info, output_dir):
        """Extract text content from document"""
        try:
            print("Extracting text content...")
            
            # Look for text content
            text_selectors = [
                '.text_layer',
                '.page_text',
                '.document_content',
                'p',
                '.text'
            ]
            
            all_text = []
            
            for selector in text_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        text = element.get_attribute('textContent') or element.text
                        if text and text.strip():
                            all_text.append(text.strip())
                except:
                    continue
            
            if not all_text:
                print("No text content found")
                return False
            
            # Save text to file
            text_file = os.path.join(output_dir, f"{doc_info['title']}.txt")
            with open(text_file, 'w', encoding='utf-8') as f:
                f.write('\n\n'.join(all_text))
            
            print(f"Text content saved to: {text_file}")
            return True
            
        except Exception as e:
            print(f"Error extracting text: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description='Download documents from Scribd')
    parser.add_argument('url', help='Scribd document URL')
    parser.add_argument('-o', '--output', default='downloads', help='Output directory')
    parser.add_argument('--no-headless', action='store_true', help='Run browser in visible mode')
    
    args = parser.parse_args()
    
    # Validate URL
    if 'scribd.com' not in args.url:
        print("Error: Please provide a valid Scribd URL")
        return
    
    # Create downloader
    downloader = ScribdDownloader(headless=not args.no_headless)
    
    print(f"Starting download from: {args.url}")
    print(f"Output directory: {args.output}")
    
    # Download document
    success = downloader.download_with_selenium(args.url, args.output)
    
    if success:
        print("\nDownload completed successfully!")
    else:
        print("\nDownload failed. Please check the URL and try again.")
        print("Note: Some documents may require a Scribd subscription to download.")

if __name__ == '__main__':
    main()