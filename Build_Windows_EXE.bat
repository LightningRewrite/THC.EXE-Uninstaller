@echo off
setlocal
cd /d "%~dp0"

echo ========================================
echo Building THC.EXE Uninstaller for Windows
echo ========================================

echo Checking for Python...
py -3 --version >nul 2>&1
if errorlevel 1 (
  echo Python 3 was not found.
  echo Install Python from https://www.python.org/downloads/windows/
  pause
  exit /b 1
)

if not exist "thc_exe_uninstaller.ico" (
  echo ERROR: thc_exe_uninstaller.ico was not found in this folder.
  pause
  exit /b 1
)

echo Installing/updating PyInstaller...
py -3 -m pip install --upgrade pyinstaller
if errorlevel 1 (
  echo Failed to install PyInstaller.
  pause
  exit /b 1
)

echo Cleaning previous build output...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist "THC.EXE Uninstaller.spec" del /q "THC.EXE Uninstaller.spec"

echo Running PyInstaller with the included ICO...
py -3 -m PyInstaller ^
  --noconfirm ^
  --clean ^
  --onefile ^
  --windowed ^
  --name "THC.EXE Uninstaller" ^
  --icon "thc_exe_uninstaller.ico" ^
  --add-data "analytics;analytics" ^
  --add-data "thc_exe_uninstaller.ico;." ^
  --hidden-import analytics.window ^
  thc_exe_uninstaller.py
if errorlevel 1 (
  echo.
  echo Build failed. Check the output above.
  pause
  exit /b 1
)

echo.
echo Creating a fresh filename to bypass Windows Explorer icon cache...
copy /y "dist\THC.EXE Uninstaller.exe" "dist\THC.EXE Uninstaller - Icon Check.exe" >nul
if errorlevel 1 (
  echo NOTE: Could not create icon-check copy.
)
echo.
echo SUCCESS: EXE is at dist\THC.EXE Uninstaller.exe
echo The executable icon is set from thc_exe_uninstaller.ico
echo The app window should also load the same ICO at runtime.
echo.
echo IMPORTANT: If Explorer still shows an old icon for the original EXE,
echo inspect "dist\THC.EXE Uninstaller - Icon Check.exe" first.
echo Windows sometimes caches icons by executable filename/path.
echo You can use the original EXE after Explorer refreshes its cache.
pause
