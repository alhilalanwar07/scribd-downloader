#!/usr/bin/env python3
"""
Scribd Downloader Package

A Python package for downloading documents from Scribd.

Author: Assistant
Version: 1.0.0
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Assistant"
__email__ = "assistant@example.com"
__license__ = "MIT"
__description__ = "A tool to download documents from Scribd"

# Import main classes and functions
try:
    from .scribd_downloader import ScribdDownloader
    from .config import (
        DEFAULT_OUTPUT_DIR,
        DEFAULT_HEADLESS,
        SELECTORS,
        validate_url,
        clean_filename
    )
    from .utils import (
        setup_logging,
        extract_document_id,
        generate_safe_filename,
        create_directory,
        save_metadata,
        load_metadata,
        validate_chrome_driver
    )
except ImportError:
    # Handle case where package is not properly installed
    import sys
    import os
    
    # Add current directory to path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    try:
        from scribd_downloader import ScribdDownloader
        from config import (
            DEFAULT_OUTPUT_DIR,
            DEFAULT_HEADLESS,
            SELECTORS,
            validate_url,
            clean_filename
        )
        from utils import (
            setup_logging,
            extract_document_id,
            generate_safe_filename,
            create_directory,
            save_metadata,
            load_metadata,
            validate_chrome_driver
        )
    except ImportError as e:
        print(f"Warning: Could not import all modules: {e}")
        ScribdDownloader = None

# Package metadata
__all__ = [
    'ScribdDownloader',
    'DEFAULT_OUTPUT_DIR',
    'DEFAULT_HEADLESS',
    'SELECTORS',
    'validate_url',
    'clean_filename',
    'setup_logging',
    'extract_document_id',
    'generate_safe_filename',
    'create_directory',
    'save_metadata',
    'load_metadata',
    'validate_chrome_driver',
    '__version__',
    '__author__',
    '__email__',
    '__license__',
    '__description__'
]

# Quick start function
def quick_download(url, output_dir="downloads", headless=True):
    """Quick download function for simple usage
    
    Args:
        url (str): Scribd document URL
        output_dir (str): Output directory for downloaded files
        headless (bool): Run browser in headless mode
    
    Returns:
        bool: True if download successful, False otherwise
    
    Example:
        >>> import scribd_downloader
        >>> success = scribd_downloader.quick_download(
        ...     "https://www.scribd.com/document/123456/example"
        ... )
    """
    if ScribdDownloader is None:
        print("Error: ScribdDownloader not available")
        return False
    
    try:
        downloader = ScribdDownloader(headless=headless)
        return downloader.download_with_selenium(url, output_dir)
    except Exception as e:
        print(f"Download failed: {e}")
        return False

# Add quick_download to __all__
__all__.append('quick_download')

# Version check function
def check_dependencies():
    """Check if all required dependencies are installed
    
    Returns:
        dict: Status of each dependency
    """
    dependencies = {
        'requests': False,
        'beautifulsoup4': False,
        'selenium': False,
        'Pillow': False,
        'lxml': False,
        'chromedriver': False
    }
    
    # Check Python packages
    for package in ['requests', 'beautifulsoup4', 'selenium', 'Pillow', 'lxml']:
        try:
            __import__(package.replace('beautifulsoup4', 'bs4').replace('Pillow', 'PIL'))
            dependencies[package] = True
        except ImportError:
            dependencies[package] = False
    
    # Check ChromeDriver
    if validate_chrome_driver:
        dependencies['chromedriver'] = validate_chrome_driver()
    
    return dependencies

def print_dependency_status():
    """Print status of all dependencies"""
    print("Scribd Downloader - Dependency Status")
    print("=" * 40)
    
    deps = check_dependencies()
    
    for dep, status in deps.items():
        status_str = "✓ OK" if status else "✗ Missing"
        print(f"{dep:<15}: {status_str}")
    
    all_ok = all(deps.values())
    print("\n" + "=" * 40)
    
    if all_ok:
        print("✓ All dependencies are installed!")
    else:
        print("✗ Some dependencies are missing.")
        print("Run: pip install -r requirements.txt")
    
    return all_ok

# Add to __all__
__all__.extend(['check_dependencies', 'print_dependency_status'])

# Package info function
def info():
    """Print package information"""
    print(f"Scribd Downloader v{__version__}")
    print(f"Author: {__author__}")
    print(f"License: {__license__}")
    print(f"Description: {__description__}")
    print()
    print("Usage:")
    print("  from scribd_downloader import ScribdDownloader")
    print("  downloader = ScribdDownloader()")
    print("  downloader.download_with_selenium(url, output_dir)")
    print()
    print("Quick usage:")
    print("  import scribd_downloader")
    print("  scribd_downloader.quick_download(url)")

__all__.append('info')

# Initialize logging if not already done
try:
    import logging
    if not logging.getLogger('scribd_downloader').handlers:
        setup_logging()
except:
    pass

# Welcome message (only show once)
if __name__ != '__main__':
    import os
    if os.environ.get('SCRIBD_DOWNLOADER_QUIET') != '1':
        # Only show on first import
        import sys
        if 'scribd_downloader' not in sys.modules:
            print(f"Scribd Downloader v{__version__} loaded successfully!")
            print("Use scribd_downloader.info() for usage information.")
            print("Use scribd_downloader.print_dependency_status() to check dependencies.")
            print()