@echo off
chcp 65001 >nul
cd /d "%~dp0"
python patch_donate_support_links.py
if errorlevel 1 (
  echo.
  echo Pythonで実行できませんでした。Windowsの場合は Python 3 を入れてください。
  pause
  exit /b 1
)
echo.
echo 完了しました。patch_donate_support_result.txt を確認してください。
pause
