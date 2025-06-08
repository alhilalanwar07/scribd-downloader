#!/usr/bin/env python3
"""
Konfigurasi untuk Scribd Downloader
"""

import os
from pathlib import Path

# Direktori default
DEFAULT_OUTPUT_DIR = "downloads"
DEFAULT_TEMP_DIR = "temp"

# Pengaturan browser
DEFAULT_HEADLESS = True
DEFAULT_WINDOW_SIZE = "1920,1080"
BROWSER_TIMEOUT = 30
PAGE_LOAD_TIMEOUT = 15

# Pengaturan download
MAX_PAGES_SCREENSHOT = 50  # Maksimal halaman untuk screenshot
MAX_RETRY_ATTEMPTS = 3
DELAY_BETWEEN_PAGES = 1  # Detik
DELAY_AFTER_CLICK = 2  # Detik

# User Agent
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

# Selectors untuk elemen halaman
SELECTORS = {
    'download_buttons': [
        'button[data-testid="download-button"]',
        '.download_button',
        'button:contains("Download")',
        'a:contains("Download")',
        '[aria-label*="download"]',
        '.btn-download',
        '#download-btn'
    ],
    'document_pages': [
        '.page',
        '.document_page',
        '[data-page]',
        '.text_layer',
        '.page-container',
        '.document-page'
    ],
    'text_content': [
        '.text_layer',
        '.page_text',
        '.document_content',
        'p',
        '.text',
        '.content-text',
        '.document-text'
    ],
    'title': [
        'h1.document_title',
        '.document-title',
        'h1',
        'title',
        '.title',
        '.doc-title'
    ]
}

# Pengaturan file output
FILE_SETTINGS = {
    'max_filename_length': 100,
    'invalid_chars': r'[<>:"/\\|?*]',
    'replacement_char': '_',
    'text_encoding': 'utf-8',
    'image_format': 'PNG',
    'image_quality': 95
}

# Chrome options
CHROME_OPTIONS = [
    '--no-sandbox',
    '--disable-dev-shm-usage',
    '--disable-gpu',
    '--disable-web-security',
    '--disable-features=VizDisplayCompositor',
    '--disable-extensions',
    '--disable-plugins',
    '--disable-images',  # Untuk mempercepat loading
    '--disable-javascript',  # Opsional, bisa diaktifkan jika diperlukan
]

# Logging configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'scribd_downloader.log',
    'max_size': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5
}

# Rate limiting
RATE_LIMIT = {
    'requests_per_minute': 30,
    'delay_between_requests': 2,  # Detik
    'max_concurrent_downloads': 1
}

# Error messages
ERROR_MESSAGES = {
    'invalid_url': "URL tidak valid. Pastikan URL dari scribd.com",
    'driver_not_found': "ChromeDriver tidak ditemukan. Silakan install ChromeDriver",
    'timeout': "Timeout saat memuat halaman. Coba lagi nanti",
    'no_content': "Tidak ada konten yang ditemukan",
    'download_failed': "Download gagal. Dokumen mungkin memerlukan subscription",
    'network_error': "Error jaringan. Periksa koneksi internet"
}

# Success messages
SUCCESS_MESSAGES = {
    'download_complete': "Download selesai!",
    'text_extracted': "Teks berhasil diekstrak",
    'screenshots_saved': "Screenshot halaman berhasil disimpan",
    'setup_complete': "Setup berhasil"
}

def get_config_dir():
    """Mendapatkan direktori konfigurasi"""
    home = Path.home()
    config_dir = home / '.scribd_downloader'
    config_dir.mkdir(exist_ok=True)
    return config_dir

def get_cache_dir():
    """Mendapatkan direktori cache"""
    cache_dir = get_config_dir() / 'cache'
    cache_dir.mkdir(exist_ok=True)
    return cache_dir

def get_log_file():
    """Mendapatkan path file log"""
    return get_config_dir() / LOGGING_CONFIG['file']

def clean_filename(filename):
    """Membersihkan nama file dari karakter tidak valid"""
    import re
    
    # Hapus karakter tidak valid
    clean_name = re.sub(
        FILE_SETTINGS['invalid_chars'], 
        FILE_SETTINGS['replacement_char'], 
        filename
    )
    
    # Batasi panjang nama file
    if len(clean_name) > FILE_SETTINGS['max_filename_length']:
        clean_name = clean_name[:FILE_SETTINGS['max_filename_length']]
    
    # Hapus spasi di awal dan akhir
    clean_name = clean_name.strip()
    
    # Pastikan tidak kosong
    if not clean_name:
        clean_name = "untitled_document"
    
    return clean_name

def validate_url(url):
    """Validasi URL Scribd"""
    if not url:
        return False, ERROR_MESSAGES['invalid_url']
    
    if 'scribd.com' not in url.lower():
        return False, ERROR_MESSAGES['invalid_url']
    
    # Cek format URL dokumen
    import re
    if not re.search(r'/document/\d+/', url):
        return False, "URL harus berupa link dokumen Scribd yang valid"
    
    return True, "URL valid"

def get_output_path(base_dir, title):
    """Mendapatkan path output yang aman"""
    clean_title = clean_filename(title)
    output_dir = Path(base_dir) / clean_title
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir

# Export semua konfigurasi
__all__ = [
    'DEFAULT_OUTPUT_DIR',
    'DEFAULT_TEMP_DIR', 
    'DEFAULT_HEADLESS',
    'DEFAULT_WINDOW_SIZE',
    'BROWSER_TIMEOUT',
    'PAGE_LOAD_TIMEOUT',
    'MAX_PAGES_SCREENSHOT',
    'MAX_RETRY_ATTEMPTS',
    'DELAY_BETWEEN_PAGES',
    'DELAY_AFTER_CLICK',
    'DEFAULT_USER_AGENT',
    'SELECTORS',
    'FILE_SETTINGS',
    'CHROME_OPTIONS',
    'LOGGING_CONFIG',
    'RATE_LIMIT',
    'ERROR_MESSAGES',
    'SUCCESS_MESSAGES',
    'get_config_dir',
    'get_cache_dir',
    'get_log_file',
    'clean_filename',
    'validate_url',
    'get_output_path'
]