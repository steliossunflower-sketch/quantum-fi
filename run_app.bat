@echo off
cd /d "%~dp0"
echo Starting Golden Ratio Quantum Pulse Visualizer...
echo.

REM Check if Streamlit is installed first
python -m streamlit --version >nul 2>&1
if errorlevel 1 (
    echo Streamlit not found. Installing...
    pip install -r requirements.txt
    echo.
)

REM Launcher finds a free port (8501-8520), starts Streamlit, and opens the browser
python run_streamlit.py
if errorlevel 1 (
    echo.
    echo To run on a specific port, use:
    echo   python -m streamlit run app.py --server.port 8521
    echo then open http://localhost:8521 in your browser.
)
echo.
pause
