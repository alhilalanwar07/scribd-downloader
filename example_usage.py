#!/usr/bin/env python3
"""
Contoh penggunaan Scribd Downloader
"""

from scribd_downloader import ScribdDownloader
import os

def example_download():
    """Contoh download dokumen dari Scribd"""
    
    # URL contoh (ganti dengan URL dokumen Scribd yang valid)
    example_urls = [
        "https://www.scribd.com/document/123456/example-document",
        # Tambahkan URL lain di sini
    ]
    
    # Buat instance downloader
    downloader = ScribdDownloader(headless=True)
    
    # Buat folder output
    output_dir = "example_downloads"
    os.makedirs(output_dir, exist_ok=True)
    
    print("=== Scribd Downloader Example ===")
    print(f"Output directory: {output_dir}")
    print()
    
    for i, url in enumerate(example_urls, 1):
        print(f"[{i}/{len(example_urls)}] Downloading: {url}")
        
        try:
            success = downloader.download_with_selenium(url, output_dir)
            
            if success:
                print(f"✓ Download berhasil!")
            else:
                print(f"✗ Download gagal!")
                
        except Exception as e:
            print(f"✗ Error: {e}")
        
        print("-" * 50)
    
    print("Selesai!")

def interactive_download():
    """Mode interaktif untuk download"""
    
    print("=== Scribd Downloader - Mode Interaktif ===")
    print()
    
    while True:
        url = input("Masukkan URL Scribd (atau 'quit' untuk keluar): ").strip()
        
        if url.lower() in ['quit', 'exit', 'q']:
            break
            
        if not url:
            print("URL tidak boleh kosong!")
            continue
            
        if 'scribd.com' not in url:
            print("URL harus dari scribd.com!")
            continue
        
        # Opsi output directory
        output = input("Output directory (default: downloads): ").strip()
        if not output:
            output = "downloads"
        
        # Opsi headless
        headless_input = input("Headless mode? (y/n, default: y): ").strip().lower()
        headless = headless_input != 'n'
        
        print(f"\nMengunduh dari: {url}")
        print(f"Output: {output}")
        print(f"Headless: {headless}")
        print()
        
        try:
            downloader = ScribdDownloader(headless=headless)
            success = downloader.download_with_selenium(url, output)
            
            if success:
                print("\n✓ Download berhasil!")
            else:
                print("\n✗ Download gagal!")
                
        except Exception as e:
            print(f"\n✗ Error: {e}")
        
        print("\n" + "="*50 + "\n")
    
    print("Terima kasih telah menggunakan Scribd Downloader!")

def test_document_info():
    """Test ekstraksi informasi dokumen"""
    
    print("=== Test Document Info Extraction ===")
    
    test_urls = [
        "https://www.scribd.com/document/123456/example-document",
        # Tambahkan URL test lain
    ]
    
    downloader = ScribdDownloader()
    
    for url in test_urls:
        print(f"\nTesting URL: {url}")
        
        try:
            info = downloader.extract_document_info(url)
            
            if info:
                print(f"Title: {info['title']}")
                print(f"Doc ID: {info['doc_id']}")
                print(f"URL: {info['url']}")
            else:
                print("Gagal mengekstrak informasi dokumen")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        
        if mode == 'example':
            example_download()
        elif mode == 'interactive':
            interactive_download()
        elif mode == 'test':
            test_document_info()
        else:
            print("Mode tidak dikenal. Gunakan: example, interactive, atau test")
    else:
        print("Pilih mode:")
        print("1. example - Download contoh")
        print("2. interactive - Mode interaktif")
        print("3. test - Test ekstraksi info")
        print()
        
        choice = input("Pilihan (1-3): ").strip()
        
        if choice == '1':
            example_download()
        elif choice == '2':
            interactive_download()
        elif choice == '3':
            test_document_info()
        else:
            print("Pilihan tidak valid!")