@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
:: WOL-MSTSC Launcher Script

echo ================================
echo WOL-MSTSC Program Start
echo ================================
echo.

:: Check and install required packages
echo Checking required packages...
python -c "import cryptography, requests" >nul 2>&1
if errorlevel 1 (
    echo.
    echo [INSTALL] Installing required Python packages...
    echo.
    python -m pip install -r requirements.txt
    echo.
)

:: Run main program
python wol_mstsc.py
set EXIT_CODE=%errorlevel%

echo.
echo ================================
echo Program Exit
echo ================================
echo.
pause

exit /b %EXIT_CODE%
