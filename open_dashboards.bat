@echo off
REM Dashboard Launcher for iLuminara Swahili AI Agents (Windows)
REM Opens all monitoring dashboards and management consoles in Chrome

echo.
echo ========================================
echo iLuminara Swahili AI - Opening Dashboards
echo ========================================
echo.

REM Check if Chrome is installed
where chrome >nul 2>nul
if %errorlevel% neq 0 (
    echo WARNING: Chrome not found in PATH. Trying default location...
    set CHROME="C:\Program Files\Google\Chrome\Application\chrome.exe"
) else (
    set CHROME=chrome
)

echo Select which dashboards to open:
echo 1) All Cloud Consoles (Dialogflow, Vertex AI, Translation, Storage)
echo 2) All Monitoring (Grafana, Prometheus, Cloud Monitoring, GitHub Actions)
echo 3) All Documentation
echo 4) Local Dashboard HTML
echo 5) Everything
echo 6) Exit
echo.

set /p choice="Enter choice [1-6]: "

if "%choice%"=="1" goto cloud
if "%choice%"=="2" goto monitoring
if "%choice%"=="3" goto docs
if "%choice%"=="4" goto dashboard
if "%choice%"=="5" goto everything
if "%choice%"=="6" goto exit
goto invalid

:cloud
echo.
echo Opening Google Cloud Consoles...
start %CHROME% "https://dialogflow.cloud.google.com/cx"
timeout /t 1 /nobreak >nul
start %CHROME% "https://console.cloud.google.com/vertex-ai"
timeout /t 1 /nobreak >nul
start %CHROME% "https://console.cloud.google.com/apis/library/translate.googleapis.com"
timeout /t 1 /nobreak >nul
start %CHROME% "https://console.cloud.google.com/storage"
goto done

:monitoring
echo.
echo Opening Monitoring Dashboards...
start %CHROME% "http://localhost:3000"
timeout /t 1 /nobreak >nul
start %CHROME% "http://localhost:9090"
timeout /t 1 /nobreak >nul
start %CHROME% "https://console.cloud.google.com/monitoring"
timeout /t 1 /nobreak >nul
start %CHROME% "https://github.com/VISENDI56/iLuminara-Core/actions"
goto done

:docs
echo.
echo Opening Documentation...
start %CHROME% "file:///%CD%/docs/google_cloud_ai_swahili_research.md"
timeout /t 1 /nobreak >nul
start %CHROME% "file:///%CD%/SWAHILI_AI_IMPLEMENTATION.md"
timeout /t 1 /nobreak >nul
start %CHROME% "file:///%CD%/TESTING.md"
timeout /t 1 /nobreak >nul
start %CHROME% "file:///%CD%/JETSON_DEPLOYMENT.md"
timeout /t 1 /nobreak >nul
start %CHROME% "file:///%CD%/DIALOGFLOW_CX_CONFIG.md"
goto done

:dashboard
echo.
echo Opening Local Dashboard...
start %CHROME% "file:///%CD%/dashboard_launcher.html"
goto done

:everything
echo.
echo Opening Everything...
echo.
echo Cloud Consoles...
start %CHROME% "https://dialogflow.cloud.google.com/cx"
timeout /t 1 /nobreak >nul
start %CHROME% "https://console.cloud.google.com/vertex-ai"
timeout /t 1 /nobreak >nul
start %CHROME% "https://console.cloud.google.com/apis/library/translate.googleapis.com"
timeout /t 1 /nobreak >nul
start %CHROME% "https://console.cloud.google.com/storage"
timeout /t 2 /nobreak >nul

echo.
echo Monitoring Dashboards...
start %CHROME% "http://localhost:3000"
timeout /t 1 /nobreak >nul
start %CHROME% "http://localhost:9090"
timeout /t 1 /nobreak >nul
start %CHROME% "https://console.cloud.google.com/monitoring"
timeout /t 1 /nobreak >nul
start %CHROME% "https://github.com/VISENDI56/iLuminara-Core/actions"
timeout /t 2 /nobreak >nul

echo.
echo Local Dashboard...
start %CHROME% "file:///%CD%/dashboard_launcher.html"
goto done

:invalid
echo.
echo Invalid choice. Exiting...
exit /b 1

:exit
echo.
echo Exiting...
exit /b 0

:done
echo.
echo ========================================
echo Done! All requested dashboards opened.
echo ========================================
echo.
echo Tip: You can also open 'dashboard_launcher.html' directly
echo      for a visual interface with all links.
echo.
pause
