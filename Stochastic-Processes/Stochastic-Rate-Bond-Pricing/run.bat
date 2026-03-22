@echo off
setlocal EnableExtensions EnableDelayedExpansion

cd /d "%~dp0"

echo =======================================
echo   ZCB Pricing Tool
echo =======================================
echo.

:: --- Path Configuration ---
set "APP_DIR=%~dp0"
set "VENV_DIR=%APP_DIR%.venv"
set "VENV_PY=%VENV_DIR%\Scripts\python.exe"
set "SETUP_FLAG=%VENV_DIR%\installed.flag"

:: --- Python Installer Configuration ---
set "PY_VERSION=3.14.3"
set "PY_URL=https://www.python.org/ftp/python/%PY_VERSION%/python-%PY_VERSION%-amd64.exe"
set "PY_INSTALLER=%TEMP%\python-%PY_VERSION%-amd64.exe"

:: Separate executable and arguments
set "PY_EXE="
set "PY_ARGS="

:: --- Pre-flight Check ---
if not exist "requirements.txt" (
    echo requirements.txt not found in:
    echo %APP_DIR%
    pause
    exit /b 1
)

:: --- Python Detection & Installation Logic ---
call :FindPython

if not defined PY_EXE (
    echo Python was not found.
    echo Downloading and installing Python %PY_VERSION% for this user...
    echo.

    powershell -NoProfile -ExecutionPolicy Bypass -Command ^
        "Invoke-WebRequest -Uri '%PY_URL%' -OutFile '%PY_INSTALLER%'"
    if errorlevel 1 (
        echo Failed to download Python.
        pause
        exit /b 1
    )

    "%PY_INSTALLER%" /quiet InstallAllUsers=0 PrependPath=1 Include_test=0 Include_pip=1 Shortcuts=0
    if errorlevel 1 (
        echo Failed to install Python.
        del "%PY_INSTALLER%" >nul 2>nul
        pause
        exit /b 1
    )

    del "%PY_INSTALLER%" >nul 2>nul

    call :FindPython
    if not defined PY_EXE (
        echo Python was installed, but could not be detected.
        pause
        exit /b 1
    )
)

:: Verify the Python version is working
echo Python ready:
if defined PY_ARGS (
    "%PY_EXE%" %PY_ARGS% --version
) else (
    "%PY_EXE%" --version
)
if errorlevel 1 (
    echo Python is not working correctly.
    pause
    exit /b 1
)
echo.

:: --- Environment Setup Logic ---
if not exist "%VENV_PY%" (
    call :SetupApp
    if errorlevel 1 exit /b 1
) else (
    if not exist "%SETUP_FLAG%" (
        call :SetupApp
        if errorlevel 1 exit /b 1
    ) else (
        echo App is already set up. Skipping installation.
    )
)

:: --- Application Launch ---
echo.
echo Launching application...
"%VENV_PY%" -m streamlit run "src\main_page.py"

echo.
echo Application closed.
pause
endlocal
exit /b 0

:: --- Subroutine: SetupApp ---
:SetupApp
echo Setting up the virtual environment...

if defined PY_ARGS (
    "%PY_EXE%" %PY_ARGS% -m venv "%VENV_DIR%"
) else (
    "%PY_EXE%" -m venv "%VENV_DIR%"
)
if errorlevel 1 (
    echo Failed to create the virtual environment.
    pause
    exit /b 1
)

echo.
echo Installing dependencies...
"%VENV_PY%" -m pip install --upgrade pip
if errorlevel 1 (
    echo Failed to upgrade pip.
    pause
    exit /b 1
)

"%VENV_PY%" -m pip install -r requirements.txt --default-timeout=100 --no-cache-dir
if errorlevel 1 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)

echo done>"%SETUP_FLAG%"
echo Setup complete.
exit /b 0

:: --- Subroutine: FindPython ---
:FindPython
set "PY_EXE="
set "PY_ARGS="

:: 1. Check for the Python Launcher (py.exe)
for /f "delims=" %%I in ('where py 2^>nul') do (
    set "PY_EXE=py"
    set "PY_ARGS=-3"
    exit /b 0
)

:: 2. Check for 'python' in the system PATH, excluding the Windows Store version
for /f "delims=" %%I in ('where python 2^>nul') do (
    echo %%I | findstr /i "WindowsApps" >nul
    if errorlevel 1 (
        set "PY_EXE=%%I"
        set "PY_ARGS="
        exit /b 0
    )
)

:: 3. Check the standard User Local Program directory
for /d %%D in ("%LocalAppData%\Programs\Python\Python*") do (
    if exist "%%~fD\python.exe" (
        set "PY_EXE=%%~fD\python.exe"
        set "PY_ARGS="
        exit /b 0
    )
)

exit /b 0