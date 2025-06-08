@echo off
echo ===================================
echo     Scribd Downloader v1.0
echo ===================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python tidak ditemukan!
    echo Silakan install Python terlebih dahulu.
    pause
    exit /b 1
)

:: Check if requirements are installed
echo Checking dependencies...
pip show requests >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Gagal menginstall dependencies!
        pause
        exit /b 1
    )
)

echo Dependencies OK!
echo.

:: Show menu
:menu
echo Pilih mode:
echo 1. Download dengan URL
echo 2. Mode Interaktif
echo 3. Contoh Penggunaan
echo 4. Exit
echo.
set /p choice="Pilihan (1-4): "

if "%choice%"=="1" goto download_url
if "%choice%"=="2" goto interactive
if "%choice%"=="3" goto example
if "%choice%"=="4" goto exit
echo Pilihan tidak valid!
goto menu

:download_url
echo.
set /p url="Masukkan URL Scribd: "
if "%url%"=="" (
    echo URL tidak boleh kosong!
    goto menu
)
echo.
set /p output="Output directory (default: downloads): "
if "%output%"=="" set output=downloads

echo.
echo Downloading from: %url%
echo Output: %output%
echo.
python scribd_downloader.py "%url%" -o "%output%"
echo.
echo Tekan tombol apa saja untuk kembali ke menu...
pause >nul
goto menu

:interactive
echo.
echo Starting interactive mode...
echo.
python example_usage.py interactive
echo.
echo Tekan tombol apa saja untuk kembali ke menu...
pause >nul
goto menu

:example
echo.
echo Running example...
echo.
python example_usage.py example
echo.
echo Tekan tombol apa saja untuk kembali ke menu...
pause >nul
goto menu

:exit
echo.
echo Terima kasih telah menggunakan Scribd Downloader!
echo.
pause
exit /b 0