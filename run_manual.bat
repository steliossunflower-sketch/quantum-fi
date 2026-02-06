@echo off
cd /d "%~dp0"
echo ============================================
echo   Phi Pulse - Manual Run (App Only)
echo ============================================
echo.
echo Starting Streamlit app at http://localhost:8876
echo Press Ctrl+C to stop.
echo.
python -m streamlit run app.py --server.port 8876
if errorlevel 1 (
    echo.
    echo Streamlit not found. Run: pip install -r requirements.txt
    pause
    exit /b 1
)
pause
