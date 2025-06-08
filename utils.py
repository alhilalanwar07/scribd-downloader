#!/usr/bin/env python3
"""
Utility functions untuk Scribd Downloader
"""

import os
import re
import time
import logging
import hashlib
from pathlib import Path
from urllib.parse import urlparse, urljoin
from datetime import datetime
import json
from typing import Optional, List, Dict, Any

def setup_logging(log_file: str = None, level: str = 'INFO') -> logging.Logger:
    """Setup logging configuration"""
    
    # Create logger
    logger = logging.getLogger('scribd_downloader')
    logger.setLevel(getattr(logging, level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if log_file specified)
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def extract_document_id(url: str) -> Optional[str]:
    """Extract document ID from Scribd URL"""
    match = re.search(r'/document/(\d+)/', url)
    return match.group(1) if match else None

def generate_safe_filename(title: str, max_length: int = 100) -> str:
    """Generate safe filename from document title"""
    
    # Remove invalid characters
    safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)
    
    # Remove extra whitespace
    safe_title = re.sub(r'\s+', ' ', safe_title).strip()
    
    # Limit length
    if len(safe_title) > max_length:
        safe_title = safe_title[:max_length].rsplit(' ', 1)[0]
    
    # Ensure not empty
    if not safe_title:
        safe_title = 'untitled_document'
    
    return safe_title

def create_directory(path: str) -> bool:
    """Create directory if it doesn't exist"""
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logging.error(f"Failed to create directory {path}: {e}")
        return False

def get_file_hash(file_path: str) -> Optional[str]:
    """Get MD5 hash of file"""
    try:
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        logging.error(f"Failed to get hash for {file_path}: {e}")
        return None

def save_metadata(doc_info: Dict[str, Any], output_dir: str) -> bool:
    """Save document metadata to JSON file"""
    try:
        metadata = {
            'title': doc_info.get('title', 'Unknown'),
            'doc_id': doc_info.get('doc_id'),
            'url': doc_info.get('url'),
            'download_date': datetime.now().isoformat(),
            'downloader_version': '1.0.0'
        }
        
        metadata_file = Path(output_dir) / 'metadata.json'
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        logging.error(f"Failed to save metadata: {e}")
        return False

def load_metadata(output_dir: str) -> Optional[Dict[str, Any]]:
    """Load document metadata from JSON file"""
    try:
        metadata_file = Path(output_dir) / 'metadata.json'
        if metadata_file.exists():
            with open(metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load metadata: {e}")
    return None

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def get_directory_size(directory: str) -> int:
    """Get total size of directory in bytes"""
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if os.path.exists(filepath):
                    total_size += os.path.getsize(filepath)
    except Exception as e:
        logging.error(f"Failed to get directory size: {e}")
    return total_size

def clean_text(text: str) -> str:
    """Clean extracted text"""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove control characters except newlines and tabs
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
    
    # Normalize line breaks
    text = re.sub(r'\r\n|\r', '\n', text)
    
    return text.strip()

def merge_text_files(input_dir: str, output_file: str) -> bool:
    """Merge multiple text files into one"""
    try:
        text_files = list(Path(input_dir).glob('*.txt'))
        if not text_files:
            return False
        
        # Sort files by name
        text_files.sort(key=lambda x: x.name)
        
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for i, txt_file in enumerate(text_files):
                if i > 0:
                    outfile.write('\n\n' + '='*50 + '\n\n')
                
                with open(txt_file, 'r', encoding='utf-8') as infile:
                    content = infile.read()
                    outfile.write(clean_text(content))
        
        return True
    except Exception as e:
        logging.error(f"Failed to merge text files: {e}")
        return False

def validate_chrome_driver() -> bool:
    """Check if ChromeDriver is available"""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(options=options)
        driver.quit()
        return True
    except Exception:
        return False

def get_chrome_version() -> Optional[str]:
    """Get Chrome browser version"""
    try:
        import subprocess
        import platform
        
        system = platform.system()
        
        if system == "Windows":
            # Try different Chrome paths on Windows
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            ]
            
            for path in chrome_paths:
                if os.path.exists(path):
                    result = subprocess.run(
                        [path, "--version"], 
                        capture_output=True, 
                        text=True
                    )
                    if result.returncode == 0:
                        return result.stdout.strip()
        
        elif system == "Darwin":  # macOS
            result = subprocess.run(
                ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--version"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return result.stdout.strip()
        
        elif system == "Linux":
            result = subprocess.run(
                ["google-chrome", "--version"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return result.stdout.strip()
    
    except Exception:
        pass
    
    return None

def progress_bar(current: int, total: int, width: int = 50) -> str:
    """Generate progress bar string"""
    if total == 0:
        return "[" + "="*width + "] 100%"
    
    progress = current / total
    filled = int(width * progress)
    bar = "=" * filled + "-" * (width - filled)
    percentage = int(progress * 100)
    
    return f"[{bar}] {percentage}% ({current}/{total})"

def retry_on_failure(max_attempts: int = 3, delay: float = 1.0):
    """Decorator for retrying functions on failure"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logging.warning(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                        time.sleep(delay)
                    else:
                        logging.error(f"All {max_attempts} attempts failed")
            
            raise last_exception
        return wrapper
    return decorator

def check_disk_space(path: str, required_mb: int = 100) -> bool:
    """Check if there's enough disk space"""
    try:
        import shutil
        free_bytes = shutil.disk_usage(path).free
        free_mb = free_bytes / (1024 * 1024)
        return free_mb >= required_mb
    except Exception:
        return True  # Assume OK if can't check

def sanitize_url(url: str) -> str:
    """Sanitize and normalize URL"""
    url = url.strip()
    
    # Add https if no protocol
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Parse and reconstruct to normalize
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

def get_timestamp() -> str:
    """Get current timestamp string"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def create_backup(file_path: str) -> bool:
    """Create backup of existing file"""
    try:
        if os.path.exists(file_path):
            backup_path = f"{file_path}.backup_{get_timestamp()}"
            import shutil
            shutil.copy2(file_path, backup_path)
            return True
    except Exception as e:
        logging.error(f"Failed to create backup: {e}")
    return False