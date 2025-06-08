#!/usr/bin/env python3
"""
Installer script untuk Scribd Downloader

Script ini akan:
1. Mengecek Python version
2. Install dependencies
3. Download ChromeDriver jika diperlukan
4. Setup konfigurasi
"""

import os
import sys
import subprocess
import platform
import zipfile
import requests
from pathlib import Path
import json

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Error: Python 3.7+ diperlukan")
        print(f"   Versi saat ini: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
    return True

def install_pip_packages():
    """Install required pip packages"""
    print("\n📦 Installing Python packages...")
    
    packages = [
        "requests>=2.28.0",
        "beautifulsoup4>=4.11.0",
        "selenium>=4.8.0",
        "Pillow>=9.4.0",
        "lxml>=4.9.0"
    ]
    
    for package in packages:
        try:
            print(f"   Installing {package}...")
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"   ✅ {package} installed")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Failed to install {package}")
            print(f"      Error: {e.stderr}")
            return False
    
    return True

def get_chrome_version():
    """Get installed Chrome version"""
    system = platform.system()
    
    try:
        if system == "Windows":
            import winreg
            # Try to get version from registry
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon")
                version, _ = winreg.QueryValueEx(key, "version")
                winreg.CloseKey(key)
                return version
            except:
                # Try alternative registry location
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Google\Chrome\BLBeacon")
                version, _ = winreg.QueryValueEx(key, "version")
                winreg.CloseKey(key)
                return version
        
        elif system == "Darwin":  # macOS
            result = subprocess.run(
                ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--version"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return result.stdout.strip().split()[-1]
        
        elif system == "Linux":
            result = subprocess.run(
                ["google-chrome", "--version"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return result.stdout.strip().split()[-1]
    
    except Exception as e:
        print(f"   Warning: Could not detect Chrome version: {e}")
    
    return None

def get_chromedriver_download_url(chrome_version):
    """Get ChromeDriver download URL for Chrome version"""
    if not chrome_version:
        return None
    
    # Extract major version
    major_version = chrome_version.split('.')[0]
    
    try:
        # Get latest ChromeDriver version for this Chrome version
        api_url = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{major_version}"
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            driver_version = response.text.strip()
            
            # Determine platform
            system = platform.system()
            machine = platform.machine().lower()
            
            if system == "Windows":
                platform_name = "win32"
            elif system == "Darwin":
                platform_name = "mac64" if "arm" not in machine else "mac64_m1"
            elif system == "Linux":
                platform_name = "linux64"
            else:
                return None
            
            download_url = f"https://chromedriver.storage.googleapis.com/{driver_version}/chromedriver_{platform_name}.zip"
            return download_url, driver_version
    
    except Exception as e:
        print(f"   Error getting ChromeDriver URL: {e}")
    
    return None, None

def download_chromedriver():
    """Download and install ChromeDriver"""
    print("\n🚗 Setting up ChromeDriver...")
    
    # Check if ChromeDriver already exists
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        
        driver = webdriver.Chrome(options=options)
        driver.quit()
        print("   ✅ ChromeDriver already installed and working")
        return True
    except:
        pass
    
    # Get Chrome version
    chrome_version = get_chrome_version()
    if not chrome_version:
        print("   ❌ Could not detect Chrome version")
        print("   Please install Google Chrome first")
        return False
    
    print(f"   Detected Chrome version: {chrome_version}")
    
    # Get download URL
    download_info = get_chromedriver_download_url(chrome_version)
    if not download_info[0]:
        print("   ❌ Could not find compatible ChromeDriver")
        return False
    
    download_url, driver_version = download_info
    print(f"   Downloading ChromeDriver {driver_version}...")
    
    try:
        # Download ChromeDriver
        response = requests.get(download_url, timeout=30)
        response.raise_for_status()
        
        # Create temp directory
        temp_dir = Path.cwd() / "temp_chromedriver"
        temp_dir.mkdir(exist_ok=True)
        
        # Save zip file
        zip_path = temp_dir / "chromedriver.zip"
        with open(zip_path, "wb") as f:
            f.write(response.content)
        
        # Extract zip
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Find chromedriver executable
        system = platform.system()
        exe_name = "chromedriver.exe" if system == "Windows" else "chromedriver"
        
        chromedriver_path = None
        for file_path in temp_dir.rglob(exe_name):
            chromedriver_path = file_path
            break
        
        if not chromedriver_path:
            print("   ❌ ChromeDriver executable not found in download")
            return False
        
        # Move to current directory
        target_path = Path.cwd() / exe_name
        chromedriver_path.replace(target_path)
        
        # Make executable on Unix systems
        if system != "Windows":
            os.chmod(target_path, 0o755)
        
        # Clean up
        import shutil
        shutil.rmtree(temp_dir)
        
        print(f"   ✅ ChromeDriver installed to {target_path}")
        
        # Test installation
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service
            
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            
            service = Service(str(target_path))
            driver = webdriver.Chrome(service=service, options=options)
            driver.quit()
            print("   ✅ ChromeDriver test successful")
            return True
        except Exception as e:
            print(f"   ❌ ChromeDriver test failed: {e}")
            return False
    
    except Exception as e:
        print(f"   ❌ Failed to download ChromeDriver: {e}")
        return False

def create_config_files():
    """Create configuration files"""
    print("\n⚙️  Creating configuration files...")
    
    # Create downloads directory
    downloads_dir = Path.cwd() / "downloads"
    downloads_dir.mkdir(exist_ok=True)
    print(f"   ✅ Created downloads directory: {downloads_dir}")
    
    # Create config directory
    config_dir = Path.home() / ".scribd_downloader"
    config_dir.mkdir(exist_ok=True)
    
    # Create user config file
    user_config = {
        "default_output_dir": str(downloads_dir),
        "headless_mode": True,
        "max_pages": 50,
        "download_timeout": 30,
        "created_by": "install.py",
        "version": "1.0.0"
    }
    
    config_file = config_dir / "config.json"
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(user_config, f, indent=2)
    
    print(f"   ✅ Created config file: {config_file}")
    
    return True

def test_installation():
    """Test the installation"""
    print("\n🧪 Testing installation...")
    
    try:
        # Test imports
        import requests
        import bs4
        import selenium
        from PIL import Image
        import lxml
        print("   ✅ All Python packages imported successfully")
        
        # Test ChromeDriver
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(options=options)
        driver.get("https://www.google.com")
        title = driver.title
        driver.quit()
        
        print("   ✅ ChromeDriver test successful")
        print(f"   ✅ Test page title: {title}")
        
        return True
    
    except Exception as e:
        print(f"   ❌ Installation test failed: {e}")
        return False

def main():
    """Main installation function"""
    print("🚀 Scribd Downloader Installation")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install pip packages
    if not install_pip_packages():
        print("\n❌ Failed to install Python packages")
        return False
    
    # Download ChromeDriver
    if not download_chromedriver():
        print("\n❌ Failed to setup ChromeDriver")
        print("   You may need to download it manually from:")
        print("   https://chromedriver.chromium.org/")
        return False
    
    # Create config files
    if not create_config_files():
        print("\n❌ Failed to create configuration files")
        return False
    
    # Test installation
    if not test_installation():
        print("\n❌ Installation test failed")
        return False
    
    print("\n" + "=" * 40)
    print("✅ Installation completed successfully!")
    print("\nYou can now use Scribd Downloader:")
    print("   python scribd_downloader.py <URL>")
    print("   python example_usage.py")
    print("   run_downloader.bat  (Windows)")
    print("\nFor help: python scribd_downloader.py --help")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n❌ Installation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Installation failed with error: {e}")
        sys.exit(1)