@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
:: WOL-MSTSC Launcher Script

echo ================================
echo WOL-MSTSC Program Start
echo ================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed
    echo Please install Python 3.8 or higher
    echo.
    pause
    exit /b 1
)

:: Check and install required packages
echo Checking required packages...
python -c "import cryptography, requests" >nul 2>&1
if errorlevel 1 (
    echo.
    echo [INSTALL] Installing required Python packages...
    echo.
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo [ERROR] Package installation failed
        echo.
        pause
        exit /b 1
    )
    echo.
    echo [DONE] Package installation completed
    echo.
)

:: Display menu
echo.
echo ================================
echo Select Menu
echo ================================
echo.
echo 1. Configure and Run (default)
echo 2. Change Master Password
echo 3. Reset Configuration
echo.
set /p MENU_CHOICE="Select (1-3, Enter=1): "

:: Set default value (if Enter pressed)
if "%MENU_CHOICE%"=="" set MENU_CHOICE=1

:: Process menu
if "%MENU_CHOICE%"=="1" (
    echo.
    echo [RUN] Configure and Run
    echo.
    python wol_mstsc.py
    set EXIT_CODE=%errorlevel%
) else if "%MENU_CHOICE%"=="2" (
    echo.
    echo [RUN] Change Master Password
    echo.
    python wol_mstsc.py --change-password
    set EXIT_CODE=%errorlevel%
) else if "%MENU_CHOICE%"=="3" (
    echo.
    echo [WARNING] Reset Configuration
    echo.
    set /p CONFIRM="Are you sure you want to delete the configuration? (yes/no): "
    if /i "!CONFIRM!"=="yes" (
        if exist config.enc (
            del config.enc
            echo.
            echo [DONE] Configuration deleted
            echo.
        ) else (
            echo.
            echo [INFO] No configuration file to delete
            echo.
        )
        set EXIT_CODE=0
    ) else (
        echo.
        echo [CANCEL] Configuration reset cancelled
        echo.
        set EXIT_CODE=0
    )
) else (
    echo.
    echo [ERROR] Invalid selection
    echo.
    set EXIT_CODE=1
)

echo.
echo ================================
echo Program Exit
echo ================================
echo.
pause

exit /b %EXIT_CODE%
