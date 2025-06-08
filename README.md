# Scribd Downloader

Sebuah tool untuk mengunduh dokumen dari Scribd menggunakan Python dan Selenium.

## Fitur

- Download dokumen dari Scribd
- Ekstraksi teks dari dokumen
- Screenshot halaman dokumen
- Support untuk berbagai format dokumen
- Mode headless dan visible browser

## Persyaratan

- Python 3.7+
- Chrome browser
- ChromeDriver

## Instalasi

1. Clone atau download repository ini
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install ChromeDriver:
   - Download ChromeDriver dari https://chromedriver.chromium.org/
   - Pastikan ChromeDriver ada di PATH atau letakkan di folder yang sama
   - Atau install via package manager:
     ```bash
     # Windows (dengan Chocolatey)
     choco install chromedriver
     
     # macOS (dengan Homebrew)
     brew install chromedriver
     
     # Linux (Ubuntu/Debian)
     sudo apt-get install chromium-chromedriver
     ```

## Penggunaan

### Command Line

```bash
# Download dokumen dengan mode headless (default)
python scribd_downloader.py "https://www.scribd.com/document/123456/example-document"

# Download dengan output directory khusus
python scribd_downloader.py "https://www.scribd.com/document/123456/example-document" -o "my_downloads"

# Download dengan browser visible (untuk debugging)
python scribd_downloader.py "https://www.scribd.com/document/123456/example-document" --no-headless
```

### Sebagai Module Python

```python
from scribd_downloader import ScribdDownloader

# Buat instance downloader
downloader = ScribdDownloader(headless=True)

# Download dokumen
url = "https://www.scribd.com/document/123456/example-document"
success = downloader.download_with_selenium(url, "downloads")

if success:
    print("Download berhasil!")
else:
    print("Download gagal!")
```

## Metode Download

Tool ini menggunakan beberapa metode untuk mengunduh dokumen:

1. **Download Button**: Mencari dan mengklik tombol download jika tersedia
2. **Screenshot Pages**: Mengambil screenshot dari setiap halaman dokumen
3. **Text Extraction**: Mengekstrak teks dari dokumen

## Output

Hasil download akan disimpan dalam folder yang ditentukan dengan struktur:

```
downloads/
├── Document_Title.txt          # Teks yang diekstrak
└── Document_Title/             # Folder screenshot
    ├── page_1.png
    ├── page_2.png
    └── ...
```

## Batasan

- Beberapa dokumen mungkin memerlukan subscription Scribd
- Kualitas download tergantung pada struktur halaman Scribd
- Rate limiting mungkin diterapkan oleh Scribd
- Tool ini hanya untuk penggunaan edukasi dan personal

## Troubleshooting

### ChromeDriver Error
```
Error setting up Chrome driver
```
**Solusi**: Pastikan ChromeDriver terinstall dan ada di PATH

### Timeout Error
```
TimeoutException
```
**Solusi**: Coba gunakan mode `--no-headless` untuk melihat apa yang terjadi di browser

### No Content Found
```
No document pages found
```
**Solusi**: Dokumen mungkin memerlukan login atau subscription

## Disclaimer

Tool ini dibuat untuk tujuan edukasi dan penggunaan personal. Pastikan Anda mematuhi Terms of Service Scribd dan hukum hak cipta yang berlaku. Pengguna bertanggung jawab penuh atas penggunaan tool ini.

## Kontribusi

Kontribusi sangat diterima! Silakan buat pull request atau laporkan bug melalui issues.

## Lisensi

MIT License - lihat file LICENSE untuk detail lengkap.