@echo off
setlocal
cd /d "%~dp0"
echo PTA merge helper (fixed ASCII version)
echo.
echo This window will stay open.
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0merge.ps1"
echo.
echo Finished. Press any key to close this window.
pause >nul
